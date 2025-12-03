from typing import Any, Dict, List, Optional, Tuple
import ast
import re
import textwrap
import csv, io

# ======= Helper functions =======
def convert_value(raw: str) -> Any:
    """
    Convert a raw string token into a Python type:
      - quoted strings -> str
      - numbers -> int or float
      - true/false -> bool
      - otherwise -> original string (stripped)
    Uses ast.literal_eval for safety (no code execution).
    """
    raw = raw.strip()
    # Normalize JSON-like booleans
    if raw.lower() == "true":  return True
    if raw.lower() == "false": return False
    try:
        # Handles "..." / '...' / 123 / 4.5
        return ast.literal_eval(raw)
    except Exception:
        # Fallback: unquoted, non-numeric tokens
        return raw.strip('"').strip("'")

def split_args(argstr: str) -> Dict[str, Any]:
    args: Dict[str, Any] = {}
    row = next(csv.reader(io.StringIO(argstr), delimiter=",", skipinitialspace=True, quotechar='"'), [])
    for field in row:
        field = field.strip()
        if not field:
            continue
        if "=" in field:
            key, val = field.split("=", 1)
            args[key.strip()] = convert_value(val)
        else:
            # bare flag -> True
            args[field] = True
    return args

# ====== Helper functions ======
def parse_action(line: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    name = None; args = None

    line = line.strip()
    if not line.startswith("Action:"):
        return None

    rest = line[len("Action:"):].strip()

    match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*\[(.*)\]\s*$", rest)
    if not match:
        return None

    name, argstr = match.groups()
    args = split_args(argstr)
    return name, args

# 2. We write a function that turn past steps into a readable history block for the prompt
def format_history(trajectory: List[Dict[str, str]]) -> str:
    """
    Each step in trajectory should have keys: 'thought', 'action', 'observation'.
    We render them in the canonical ReAct order for the next prompt.
    """
    lines: List[str] = []
    for step in trajectory:
        lines.append(f"Thought: {step['thought']}")
        lines.append(f"Action: {step['action']}")
        lines.append(f"Observation: {step['observation']}")
    return "\n".join(lines)


# 3. We will build the prompt shown to the model for the next step
SYSTEM_PREAMBLE = textwrap.dedent("""\
You are a helpful ReAct agent that helps users find adoptable pets.
You can use tools to search for pets based on their description, breed, age, species, location, and other attributes.

Available tools:
- search[query="<text>", species="<species>", k=<int>]  # searches the pet database and returns the top-k matching animals
  Default to k=3. Do not adjust unless absolutely necessary.
To finish, use: finish[answer="<final answer>"]

Follow the exact step format:
Thought: <your reasoning>
Action: <one of the tool calls above, or finish[...]>

Do not repeat a search with the exact same query if it has already been performed in this session.

### QUERY RULES
- Include **all descriptive words** from the user query in your search including personality traits.
  All information must go inside the `query` parameter. 
  Do **NOT** add extra parameters to the search tools
  For example, "young cuddly calico cat Boston" must appear exactly in the search query.
- Always enforce species using the species parameter.
- Example search call:
  search[query="young cuddly calico Boston", species="cat", k=3]

### FINAL ANSWER FORMAT
- Only produce the final answer inside finish[answer="..."]
- Format each result using only attributes returned by the search results. 
- Number the results:
  I have found <N> cats that match your description:  1. <name> — <age>, <breed> in <location>. <description> 2. <name> — <age>, <breed> in <location>. <description>
- Only use attributes returned by the search results. Do NOT infer missing data.
- Never merge animals into a single sentence or claim shared traits unless explicitly true.

IMPORTANT: Do not output the final answer before calling finish[...]. Only output your reasoning and Action steps before that.
""").strip()


def make_prompt(user_query: str, trajectory: List[Dict[str, str]]) -> str:
    """
    Build a prompt for the LLM including user query, history, and instructions.
    Ensures all descriptive words from the user query are preserved in the search query.
    """
    history_block = format_history(trajectory)

    prompt = (
        f"{SYSTEM_PREAMBLE}\n\n"
        f"User Question: {user_query}\n\n"
        f"{history_block}\n"
        f"Next step:\n"
        f"Thought:"
    )
    return prompt

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
    Prioritize returning accurate and relevant information to the user.

    Available tools:
    - search[query="<text>", k=<int>]  # searches the pet data base and returns the top-k matching animals
    To finish, use: finish[answer="<final answer>"]

    Follow the exact step format:
    Thought: <your reasoning>
    Action: <one of the tool calls above, or finish[...]>
    
    Example:
    User Question: "I want a calico cat who is young and cuddly"
    Thought: I should identify the species, breed, age, and personality preferences from the query before searching.
    Action: search[query="calico cat young cuddly", k=3]
    Observation: {"results":[...]}
""").strip()

def make_prompt(user_query: str, trajectory: List[Dict[str, str]]) -> str:
    history_block = format_history(trajectory)
    return (
        f"{SYSTEM_PREAMBLE}\n\n"
        f"User Question: {user_query}\n\n"
        f"{history_block}\n"
        f"Next step:\n"
        f"Thought:"
    )
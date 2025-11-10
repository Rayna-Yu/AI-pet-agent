import re, torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

MODEL_NAME   = "Qwen/Qwen2.5-0.5B-Instruct"    
LOAD_8BIT    = False                           
DTYPE        = torch.bfloat16 if torch.cuda.is_available() else torch.float32
MAX_NEW_TOKENS = 160
GENERATION_KWARGS = {}

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            device_map="auto",
            torch_dtype=DTYPE,
            trust_remote_code=True,
            attn_implementation="eager",
            **({"load_in_8bit": True} if LOAD_8BIT else {})
        )

gen_cfg = GenerationConfig(
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=GENERATION_KWARGS.get("temperature", 0.3),
            do_sample=GENERATION_KWARGS.get("do_sample", True)
        )

T_PATTERN = re.compile(r"Thought:\s*(.+)")
A_PATTERN = re.compile(r"Action:\s*(.+)")

def _postprocess_to_two_lines(text: str) -> str:
    """
    Extract the first 'Thought:' and 'Action:' lines from the model output.
    If the model drifts, fall back to a conservative default Action.
    """
    text = text.split("\nObservation:")[0]
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]

    # Try to find explicit Thought/Action anywhere in the output
    thought = None
    action  = None
    for ln in lines:
        if thought is None:
            m = T_PATTERN.match(ln)
            if m:
                thought = m.group(1).strip()
                continue
        if action is None:
            m = A_PATTERN.match(ln)
            if m:
                action = m.group(1).strip()
                continue

    # Fallbacks if the model didn’t comply perfectly
    if thought is None:
        thought = "I should search for key facts related to the question."
    if action is None:
        action = 'search[query="(auto) refine the user question", k=3]'

    return f"Thought: {thought}\nAction: {action}"



def hf_llm(prompt: str) -> str:
    """
    Completes from your existing ReAct prompt and returns exactly two lines:
    'Thought: ...' and 'Action: ...'
    """
    # We add a strong instruction to the prompt to improve compliance with the format
    format_guard = (
        "\n\nIMPORTANT: Respond with EXACTLY two lines in this format:\n"
        "Thought: <one concise sentence>\n"
        "Action: <either search[query=\"...\"] or finish[answer=\"...\"]>\n"
        "Do NOT include Observation."
    )
    full_prompt = prompt + format_guard

    inputs = tokenizer(full_prompt, return_tensors="pt")
    with torch.no_grad():
        output_ids = model.generate(**inputs, generation_config = gen_cfg)


    completion = tokenizer.decode(output_ids[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)

    return _postprocess_to_two_lines(completion)

LLM = hf_llm
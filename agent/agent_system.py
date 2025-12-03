from dataclasses import dataclass, field, asdict
from typing import Callable, Dict, List, Tuple, Optional, Any
import json, math, re, textwrap, random, os, sys
import math
from collections import Counter, defaultdict

@dataclass
class Step:
    thought: str
    action: str
    observation: str

@dataclass
class AgentConfig:
    max_steps: int = 3
    allow_tools: Tuple[str, ...] = ("search",)
    verbose: bool = True

class ReActAgent:
    def __init__(self, llm: Callable[[str], str], tools: Dict[str, Dict[str, Any]], config: AgentConfig | None=None):
        self.llm = llm
        self.tools = tools
        self.config = config or AgentConfig()
        self.trajectory: List[Step] = []

    def run(self, user_query: str) -> Dict[str, Any]:
        self.trajectory.clear()
        for step_idx in range(self.config.max_steps):
            # 1. At each step, format the prompt based on the make_prompt function and self.trajectory
            prompt = make_prompt(user_query, [asdict(s) for s in self.trajectory])

            # 2. Use self.llm to process the prompt
            out = self.llm(prompt)

            # Expect two lines: Thought:..., Action:...
            t_match = re.search(r"Thought:\s*(.*)", out)
            a_match = re.search(r"Action:\s*(.*)", out)
            thought = t_match.group(1).strip() if t_match else "(no thought)"
            action_line = a_match.group(0).strip() if a_match else 'Action: finish[answer="(no action)"]'

            #action_line = "Action: " + action_line


            # 3. Parse the action of the action line using the parse_action function
            parsed = parse_action(action_line)

            if not parsed:
                observation = "Invalid action format. Stopping."
                self.trajectory.append(Step(thought, action_line, observation))
                break
            name, args = parsed


            if name == "finish":
                observation = "done"
                self.trajectory.append(Step(thought, action_line, observation))
                break

            if name not in self.config.allow_tools or name not in self.tools:
                observation = f"Action '{name}' not allowed or not found."
                self.trajectory.append(Step(thought, action_line, observation))
                break

            # 4. Execute the action
            try:
                obs_payload = self.tools[name]["fn"](**args)
                observation = json.dumps(obs_payload, ensure_ascii=False)  # show structured obs
            except Exception as e:
                observation = f"Tool error: {e}"

            self.trajectory.append(Step(thought, action_line, observation))

        # Build final answer from last finish action if present
        final_answer = None
        for s in reversed(self.trajectory):
            if "finish[" in s.action:
                m = re.search(r'answer=["\'](.*?)["\']', s.action)
                if m:
                    final_answer = m.group(1)
                    break

        return {
            "question": user_query,
            "final_answer": final_answer,
            "steps": [asdict(s) for s in self.trajectory]
        }
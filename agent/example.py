from knowledge_base import TOOLS
from language_model import hf_llm
from agent_system import ReActAgent

agent = ReActAgent(llm=hf_llm, tools=TOOLS, config=None)

result = agent.run("I'm looking for a friendly dog in the Boston area.")

# Inspect the final answer and trajectory
print("Final answer:", result["final_answer"])
for step in result["steps"]:
    print(step["thought"])
    print(step["action"])
    print(step["observation"])
    print("---")

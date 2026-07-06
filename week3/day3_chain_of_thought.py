"""
Week 3 - Day 3: Chain-of-Thought — Make Claude Reason Step by Step
====================================================================
Goal: See how asking Claude to think step by step gives deeper,
      more reliable analysis than asking for a direct answer.
"""

import anthropic
import json

client = anthropic.Anthropic()

def get_text(message):
    for block in message.content:
        if block.type == "text":
            return block.text.strip()
    return "NO_RESPONSE"


# --- Scenario 1 ---
scenario_1 = "Should I invest in Singapore REITs given that interest rates are rising but DPU (distribution per unit) growth remains strong at 5-7%?"

# Direct prompt — just ask for the answer
# TODO: Send scenario_1 to Claude with a direct prompt:
#   "Answer this investment question in 2-3 sentences: {scenario_1}"
# Store in direct_1

direct_1_msg = client.messages.create(
    model = "claude-sonnet-5",
    max_tokens= 1024,
    messages=[{"role": "user", "content": f"Answer this investment question in 2-3 sentences: {scenario_1}"}]
)
direct_1 = get_text(direct_1_msg)


# Chain-of-thought prompt — ask Claude to reason step by step
# TODO: Send the same scenario_1 but ask Claude to think through it:
#   "Think through this step by step before giving your conclusion.
#    Step 1: How do rising interest rates affect REITs?
#    Step 2: What does strong DPU growth of 5-7% signal?
#    Step 3: What are the key risks?
#    Step 4: What is your conclusion and why?
#
#    Question: {scenario_1}"
# Store in cot_1
cot_1_msg = client.messages.create(
    model = "claude-sonnet-5",
    max_tokens=2048,
    messages=[{"role": "user", "content": f"""Think through this step by step before giving your conclusion.
Step 1: How do rising interest rates affect REITs?
Step 2: What does strong DPU growth of 5-7% signal?
Step 3: What are the key risks?
Step 4: What is your conclusion and why?  

Question: {scenario_1}"""}]            
)
cot_1 = get_text(cot_1_msg)


# --- Scenario 2 ---
scenario_2 = "A Singapore tech startup is burning $2M/month with $15M in the bank, but revenue is growing 20% month-over-month from a $500K base. Should VCs invest in the next round?"

# TODO: Direct prompt for scenario_2 — same pattern as above
# Store in direct_2
direct_2_msg = client.messages.create(
    model = "claude-sonnet-5",
    max_tokens= 1024,
    messages=[{"role": "user", "content": f"Answer this investment question in 2-3 sentences: {scenario_2}"}]
)
direct_2 = get_text(direct_2_msg)


# TODO: Chain-of-thought for scenario_2 — ask Claude to think through:
#   Step 1: Calculate the runway (how many months of cash left?)
#   Step 2: Project revenue growth at 20% MoM for the next 6 months
#   Step 3: When does revenue cover the burn rate?
#   Step 4: What are the risks?
#   Step 5: Conclusion — invest or pass?
# Store in cot_2

cot_2_msg = client.messages.create(
    model = "claude-sonnet-5",
    max_tokens=2048,
    messages=[{"role": "user", "content": f"""Think through this step by step before giving your conclusion.
Step 1: Calculate the runway (how many months of cash left?)
Step 2: Project revenue growth at 20% MoM for the next 6 months
Step 3: When does revenue cover the burn rate?
Step 4: What are the risks?
Step 5: Conclusion — invest or pass?
Question: {scenario_2}"""}]            
)
cot_2 = get_text(cot_2_msg)



# --- Print comparisons ---
# TODO: Print both scenarios showing direct vs chain-of-thought
# Use this format:
print("SCENARIO 1")
print("=" * 60)
print("\nDIRECT:")
print(direct_1)
print("\nCHAIN-OF-THOUGHT:")
print(cot_1)

print("SCENARIO 2")
print("=" * 60)
print("\nDIRECT:")
print(direct_2)
print("\nCHAIN-OF-THOUGHT:")
print(cot_2)



# --- Save results ---
# TODO: Save all results to "cot_comparison.json"
results = {
    "scenario_1": {"direct": direct_1, "chain_of_thought": cot_1},
    "scenario_2": {"direct": direct_2, "chain_of_thought": cot_2}
}
with open("cot_comparison.json", "w") as f:
    json.dump(results, f, indent=2)
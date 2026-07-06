"""
Week 3 - Saturday: Financial Research Assistant
================================================
Goal: Combine everything from Week 3 into an interactive research tool.
      - Prompt library (Day 5)
      - Chain-of-thought for complex questions (Day 3)
      - Output formatting (Day 4)
      - Temperature control (Day 1)
      - System prompts & multi-turn conversation (Week 2)
      - Token/cost tracking (Week 2)
"""

import anthropic
import json

client = anthropic.Anthropic()

def get_text(message):
    for block in message.content:
        if block.type == "text":
            return block.text.strip()
    return "NO_RESPONSE"


# ============================================================
# PART 1: Prompt Library (from Day 5)
# ============================================================
# TODO: Create prompt_library dictionary with these templates.
#   Copy your 5 templates from day5_prompt_library.py:
#   "sentiment_analysis", "risk_assessment", "earnings_summary",
#   "comparison", "explain_simple"
#
#   Add one NEW template:
#   "general_analysis":
#       """Think through this step by step before giving your conclusion.
#       Consider multiple angles and provide a balanced analysis.
#       Question: {question}"""

prompt_library = {
    "sentiment_analysis":
    """Classify the sentiment of this financial headline as BULLISH, BEARISH, or NEUTRAL.
    Also provide a confidence score from 0-100.
    Return ONLY JSON: {{"sentiment": "...", "confidence": ..., "reasoning": "..."}}
    Headline: {headline}""",

   "risk_assessment":
    """Identify the top 3 risks in this financial scenario. For each risk, rate severity
    as HIGH, MEDIUM, or LOW and explain why.
    Return as a numbered list.
    Scenario: {scenario}""",

    "earnings_summary":
    """Summarize these quarterly earnings into 4 key metrics:
    1. Revenue performance (growth/decline and why)
    2. Profitability (margins and efficiency)
    3. Risk indicators (NPL, leverage, etc.)
    4. Outlook (one sentence forward-looking view)
    Keep each point to 1-2 sentences.
    Earnings data: {earnings_data}""",

    "comparison":
    """Compare these two investment options. Give pros and cons for each,
    then a recommendation with reasoning.
    Option A: {option_a}
    Option B: {option_b}""",

    "explain_simple":
    """Explain this financial concept in simple terms that a beginner investor
    would understand. Use an everyday analogy. Keep it under 100 words.
    Concept: {concept}""",

    "general_analysis":
    """Think through this step by step before giving your conclusion.
    Consider multiple angles and provide a balanced analysis.
    Question: {question}"""
}


# ============================================================
# PART 2: Auto-detect query type
# ============================================================
# TODO: Create a function called detect_query_type(user_input)
#   - It checks the user's input for keywords to pick the right template
#   - Use simple if/elif with keyword matching:
#
#   def detect_query_type(user_input):
#       text = user_input.lower()
#       if any(word in text for word in ["sentiment", "headline", "bullish", "bearish"]):
#           return "sentiment_analysis"
#       elif any(word in text for word in ["risk", "danger", "threat"]):
#           return "risk_assessment"
#       elif any(word in text for word in ["earnings", "quarter", "q1", "q2", "q3", "q4", "revenue", "profit"]):
#           return "earnings_summary"
#       elif any(word in text for word in ["compare", "versus", "vs", "or"]):
#           return "comparison"
#       elif any(word in text for word in ["explain", "what is", "what are", "how does"]):
#           return "explain_simple"
#       else:
#           return "general_analysis"

def detect_query_type(user_input):
    text = user_input.lower()
    if any(word in text for word in ["sentiment", "headline", "bullish", "bearish"]):
        return "sentiment_analysis"
    elif any(word in text for word in ["risk", "danger", "threat"]):
        return "risk_assessment"
    elif any(word in text for word in ["earnings", "quarter", "q1", "q2", "q3", "q4", "revenue", "profit"]):
        return "earnings_summary"
    elif any(word in text for word in ["compare", "versus", "vs", "or"]):
        return "comparison"
    elif any(word in text for word in ["explain", "what is", "what are", "how does"]):
        return "explain_simple"
    else:
        return "general_analysis"



# ============================================================
# PART 3: Pick the right temperature
# ============================================================
# TODO: Create a function called pick_temperature(query_type)
#   - Returns a float based on the query type:
#
#   def pick_temperature(query_type):
#       if query_type in ["sentiment_analysis", "earnings_summary"]:
#           return 0.0    # factual — need consistency
#       elif query_type in ["risk_assessment", "comparison"]:
#           return 0.3    # some creativity for brainstorming risks
#       else:
#           return 0.5    # general/explain — balanced

def pick_temperature(query_type):
    if query_type in ["sentiment_analysis", "earnings_summary"]:
        return 0.0    # factual — need consistency
    elif query_type in ["risk_assessment", "comparison"]:
        return 0.3    # some creativity for brainstorming risks
    else:
        return 0.5    # general/explain — balanced


# ============================================================
# PART 4: Run a query through the assistant
# ============================================================
# TODO: Create a function called run_query(user_input, conversation_history)
#   This is the main function that ties everything together.
#
#   def run_query(user_input, conversation_history):
#       # Step 1: Detect query type
#       query_type = detect_query_type(user_input)
#
#       # Step 2: Pick temperature
#       temp = pick_temperature(query_type)
#
#       # Step 3: Build the prompt
#       #   If query_type is in prompt_library, fill the template
#       #   For templates with specific placeholders (like {headline}),
#       #   just pass the whole user_input as the placeholder value.
#       #   Example: if query_type == "sentiment_analysis":
#       #       prompt = prompt_library[query_type].format(headline=user_input)
#       #   For "general_analysis":
#       #       prompt = prompt_library[query_type].format(question=user_input)
#       #   For others, pass user_input as the main placeholder:
#       #       "risk_assessment" -> format(scenario=user_input)
#       #       "earnings_summary" -> format(earnings_data=user_input)
#       #       "explain_simple" -> format(concept=user_input)
#       #       "comparison" -> format(option_a=user_input, option_b="(see above)")
#
#       # Step 4: Add to conversation history
#       conversation_history.append({"role": "user", "content": prompt})
#
#       # Step 5: Send to Claude
#       #   model = "claude-sonnet-4-6" (need this for temperature support)
#       #   max_tokens = 2048
#       #   temperature = temp
#       #   system = (see PART 5 below for the system prompt)
#       #   messages = conversation_history
#
#       # Step 6: Get the response text
#       response_text = get_text(message)
#
#       # Step 7: Add assistant response to conversation_history
#       conversation_history.append({"role": "assistant", "content": response_text})
#
#       # Step 8: Calculate tokens and cost
#       #   input_tokens = message.usage.input_tokens
#       #   output_tokens = message.usage.output_tokens
#       #   cost = (input_tokens * 3 / 1_000_000) + (output_tokens * 15 / 1_000_000)
#       #   (these are claude-sonnet-4-6 prices: $3/M input, $15/M output)
#
#       # Step 9: Return a dictionary with all the info
#       #   return {
#       #       "query_type": query_type,
#       #       "temperature": temp,
#       #       "response": response_text,
#       #       "input_tokens": input_tokens,
#       #       "output_tokens": output_tokens,
#       #       "cost": cost
#       #   }

def run_query(user_input, conversation_history):
    # Step 1: Detect query type
    query_type = detect_query_type(user_input)

    # Step 2: Pick temperature
    temp = pick_temperature(query_type)

    # Step 3: Build the prompt
    if query_type == "sentiment_analysis":
        prompt = prompt_library[query_type].format(headline=user_input)
    elif query_type == "risk_assessment":
        prompt = prompt_library[query_type].format(scenario=user_input)
    elif query_type == "earnings_summary":
        prompt = prompt_library[query_type].format(earnings_data=user_input)
    elif query_type == "comparison":
        prompt = prompt_library[query_type].format(option_a=user_input, option_b="(see above)")
    elif query_type == "explain_simple":
        prompt = prompt_library[query_type].format(concept=user_input)
    else:
        prompt = prompt_library[query_type].format(question=user_input)

    # Step 4: Add to conversation history
    conversation_history.append({"role": "user", "content": prompt})

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        temperature=temp,
        system=system_prompt,
        messages=conversation_history
    )
    
    response_text = get_text(message)

    conversation_history.append({"role": "assistant", "content": response_text})

    #Step 8: Calculate tokens and cost
    input_tokens = message.usage.input_tokens
    output_tokens = message.usage.output_tokens
    cost = (input_tokens * 3 / 1_000_000) + (output_tokens * 15 / 1_000_000)

    # Step 9: Return a dictionary with all the info
    return {
        "query_type": query_type,
        "temperature": temp,
        "response": response_text,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost": cost
    }


# ============================================================
# PART 5: System prompt
# ============================================================
# TODO: Create a system prompt string for the research assistant:
#
system_prompt = """You are a senior financial research analyst at a Singapore-based
investment firm. You specialize in ASEAN markets, particularly SGX-listed equities,
REITs, and fixed income. You provide clear, data-driven analysis with specific
numbers and actionable insights. When uncertain, you say so. You always consider
both bull and bear cases."""



# ============================================================
# PART 6: Interactive loop
# ============================================================
# TODO: Build the main loop that lets you chat with the assistant.
#
print("=" * 60)
print("FINANCIAL RESEARCH ASSISTANT")
print("=" * 60)
print("Type your question. Type 'quit' to exit.\n")
#
conversation_history = []
session_log = []
#
while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["quit", "exit", "q"]:
        break
    if not user_input:
        continue
#
    result = run_query(user_input, conversation_history)

    # Print the response
    print(f"\n{'─' * 60}")
    print(result["response"])
    print(f"{'─' * 60}")
    print(f"Template: {result['query_type']} | Temp: {result['temperature']} | "
          f"Tokens: {result['input_tokens']}+{result['output_tokens']} | "
          f"Cost: ${result['cost']:.4f}")
    print()
#
    # Add to session log
    session_log.append({
        "question": user_input,
        **result
    })
#
# Save session when user quits
if session_log:
    with open("research_session.json", "w") as f:
        json.dump(session_log, f, indent=2)
    print(f"\nSession saved! {len(session_log)} queries logged.")

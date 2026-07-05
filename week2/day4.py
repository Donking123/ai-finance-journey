"""
Week 2 - Day 4: Multi-Turn Conversations — Claude Remembers Context
=====================================================================
Goal: Learn how to build conversations where Claude remembers
      what was said before. This is how chatbots and advisors work.
"""

import anthropic
import json

client = anthropic.Anthropic()

system_prompt = "You are a licensed financial advisor in Singapore. Keep responses concise — 3-4 paragraphs max."

# This list will hold the FULL conversation history
conversation = []

# --- Turn 1 ---
# TODO: Add a user message to conversation:
#   "I have $50,000 SGD to invest. I'm 28, moderate risk tolerance, and I want to grow wealth over 10 years."
# Then send it to Claude and print the response.
# After getting the response, add Claude's reply to conversation too.
#
# Pattern:
#   conversation.append({"role": "user", "content": "your message"})
#   message = client.messages.create(
#       model="claude-sonnet-5",
#       max_tokens=1024,
#       system=system_prompt,
#       messages=conversation
#   )
#   reply = next(block.text for block in message.content if block.type == "text")
#   conversation.append({"role": "assistant", "content": reply})
#   print(reply)

conversation.append({"role": "user", "content": "I have $50,000 SGD to invest. I'm 28, moderate risk tolerance, and I want to grow wealth over 10 years."})
message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    system=system_prompt,
    messages=conversation
)
reply = next(block.text for block in message.content if block.type == "text")
conversation.append({"role": "assistant", "content": reply})

print("TURN 1")
print("=" * 50)
print(reply)
print()



# --- Turn 2 ---
# TODO: Add another user message to conversation:
#   "What do you think about putting 30% into Singapore REITs?"
# Send to Claude (it now sees Turn 1 + Turn 2) and print the response.
# Don't forget to append Claude's reply to conversation.

conversation.append({"role": "user", "content": "What do you think about putting 30% into Singapore REITs?"})
message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    system=system_prompt,
    messages=conversation
)
reply = next(block.text for block in message.content if block.type == "text")
conversation.append({"role": "assistant", "content": reply})

print("TURN 2")
print("=" * 50)
print(reply)
print()

# --- Turn 3 ---
conversation.append({"role": "user", "content": "Which specific Singapore REITs would you recommend and why?"})
message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    system=system_prompt,
    messages=conversation
)
reply = next(block.text for block in message.content if block.type == "text")
conversation.append({"role": "assistant", "content": reply})

print("TURN 3")
print("=" * 50)
print(reply)
print()

# --- Print the full conversation ---
print("\n" + "=" * 60)
print("FULL CONVERSATION")
print("=" * 60)
for msg in conversation:
    print(f"\n{msg['role'].upper()}:")
    print(msg['content'])

# --- Save the conversation ---
with open("advisor_conversation.json", "w") as f:
    json.dump(conversation, f, indent=2)
print("\nSaved to advisor_conversation.json")

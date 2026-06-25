import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat(system: str, user: str, temperature: float = 0.3) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content

# ─── Demo 1: Zero-shot vs Few-shot ─────────────────────────────────
print("=== Zero-shot vs Few-shot ===\n")

zero_shot_system = "Classify the sentiment of the given text."
few_shot_system = """Classify the sentiment of the given text.

Examples:
'This framework is incredibly powerful' → positive
'Worst documentation I have ever seen' → negative
'It works but could be better' → neutral

Respond with only one word: positive, negative, or neutral."""

text = "LangChain has a steep learning curve but the results are worth it"

print(f"Text: '{text}'")
print(f"Zero-shot: {chat(zero_shot_system, text)}")
print(f"Few-shot:  {chat(few_shot_system, text)}\n")

# ─── Demo 2: Chain of Thought ───────────────────────────────────────
print("=== Chain of Thought ===\n")

normal_system = "Answer the question."
cot_system = "Think through this step by step, show your reasoning, then give the final answer."

question = "A vector database has 1 million documents. Each embedding is 384 dimensions of float32. How much memory does this require in GB?"

print(f"Question: {question}\n")
print(f"Normal answer:\n{chat(normal_system, question)}\n")
print(f"CoT answer:\n{chat(cot_system, question)}\n")

# ─── Demo 3: Structured Output ──────────────────────────────────────
print("=== Structured JSON Output ===\n")

json_system = """You are a code review assistant.
Analyze the given code and respond ONLY with a JSON object.
No explanation, no markdown, no extra text — just the raw JSON.

JSON format:
{
  "quality_score": <number 1-10>,
  "issues": [<list of issues>],
  "improvements": [<list of improvements>],
  "summary": "<one sentence summary>"
}"""

code = """
def get_user(id):
    db = connect_to_database()
    user = db.query("SELECT * FROM users WHERE id = " + id)
    return user
"""

response = chat(json_system, f"Review this code:\n{code}")
print(f"Raw response:\n{response}\n")

try:
    parsed = json.loads(response)
    print(f"Quality Score: {parsed['quality_score']}/10")
    print(f"Issues: {parsed['issues']}")
    print(f"Summary: {parsed['summary']}")
except json.JSONDecodeError:
    print("Model didn't return valid JSON — adjust the prompt")

# ─── Demo 4: Findly System Prompt ───────────────────────────────────
print("\n=== Findly Production Prompt ===\n")

FINDLY_SYSTEM_PROMPT = """You are Findly, an intelligent search assistant.

Your job:
- Answer questions using ONLY the provided search results
- Be concise and direct
- Always cite which result your answer comes from
- If the answer is not in the results, say exactly: "I couldn't find relevant information for this query."
- Never make up information

Response format:
ANSWER: <your answer>
SOURCE: <which result you used>"""

search_results = """
Result 1: Python's garbage collector uses reference counting as its primary mechanism
Result 2: The gc module provides functions to enable, disable and tune the garbage collector
Result 3: Circular references require a cyclic garbage collector to detect and clean up
"""

question = "How does Python's garbage collector work?"
response = chat(FINDLY_SYSTEM_PROMPT, f"Search results:\n{search_results}\n\nQuestion: {question}")
print(f"Q: {question}")
print(f"A: {response}")
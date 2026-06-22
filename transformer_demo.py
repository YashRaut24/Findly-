import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_with_temperature(prompt, temperature):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=100
    )
    return response.choices[0].message.content

# ─── Demo 1: Temperature Effect ────────────────────────────────────
prompt = "Complete this sentence in one line: The future of AI is"

print("=== Temperature Effect ===\n")
for temp in [0.0, 0.7, 1.5]:
    print(f"Temperature {temp}:")
    print(f"  {generate_with_temperature(prompt, temp)}\n")

# ─── Demo 2: Autoregressive Generation (simulated) ─────────────────
print("=== Token by Token Generation ===\n")

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Count from 1 to 5, one number per line."}],
    max_tokens=50,
    stream=True  # stream tokens as they generate
)

print("Streaming output:")
for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print("\n")

# ─── Demo 3: Context Window Effect ─────────────────────────────────
print("=== Context Window Demo ===\n")

# Multi-turn conversation — model uses all previous context
messages = [
    {"role": "user", "content": "My name is Yash."},
    {"role": "assistant", "content": "Nice to meet you, Yash!"},
    
    {"role": "user", "content": "My favourite programming language is Python."},
    {"role": "assistant", "content": "Python is a great choice!"},
    
    {"role": "user", "content": "I am currently learning Machine Learning."},
    {"role": "assistant", "content": "That sounds exciting!"},
    
    {"role": "user", "content": "Can you summarize everything you know about me from this conversation?"}
]

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=messages,
    max_tokens=100
)

print(f"Model summary: {response.choices[0].message.content}")
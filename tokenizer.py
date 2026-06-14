import tiktoken

# Load the tokenizer used by GPT-4 and many modern models
encoder = tiktoken.get_encoding("cl100k_base")

# Tokenize a simple sentence
text = "Hello, I am learning about tokenization in AI."
tokens = encoder.encode(text)

print(f"Original text: {text}")
print(f"Number of tokens: {len(tokens)}")
print(f"Token IDs: {tokens}")

# Decode back to text
decoded = encoder.decode(tokens)
print(f"Decoded back: {decoded}")

# See each token as text
print("\nToken breakdown:")
for token_id in tokens:
    token_text = encoder.decode([token_id])
    print(f"  {token_id} → '{token_text}'")

def count_tokens(text: str) -> int:
    """Count tokens in a string — useful for managing context windows."""
    encoder = tiktoken.get_encoding("cl100k_base")
    return len(encoder.encode(text))

def is_within_limit(text: str, limit: int = 4096) -> bool:
    """Check if text fits within a token limit."""
    return count_tokens(text) < limit

# Test it
sample = "This is a sample document that we want to send to an LLM."
print(f"\nToken count: {count_tokens(sample)}")
print(f"Within 4096 limit: {is_within_limit(sample)}")
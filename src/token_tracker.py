import tiktoken

def count_tokens(content, model="gpt-6-astra-sim"):

    try:
        encoder = tiktoken.encoding_for_model(model)

        tokens = encoder.encode(content)

        return len(tokens)

    except Exception as e:
        print(f"Warning: Failed to count tokens ({e}). Falling back to estimate.")
        return len(content) // 4
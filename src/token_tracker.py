import tiktoken


def count_tokens(content, model="gpt-4o-mini"):
    """Conta os tokens do texto usando o tokenizador do modelo."""
    encoder = tiktoken.encoding_for_model(model)

    tokens = encoder.encode(
        content,
        disallowed_special=(),
    )

    return len(tokens)
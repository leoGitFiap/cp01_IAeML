"""Conta os tokens dos textos usando tiktoken, sem acessar uma API de geração."""

import tiktoken


def contar_tokens(conteudo, modelo="gpt-4o-mini"):
    """Conta os tokens do texto usando o tokenizador do modelo."""
    # Seleciona a codificação associada ao nome do modelo.
    codificador = tiktoken.encoding_for_model(modelo)

    # Trata possíveis marcadores especiais como texto comum do currículo.
    tokens = codificador.encode(
        conteudo,
        disallowed_special=(),
    )

    # Falhas são propagadas; não há estimativa por número de caracteres.
    return len(tokens)
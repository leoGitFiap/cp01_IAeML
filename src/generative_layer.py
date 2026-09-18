"""Gera pareceres por regras locais e estima o custo dos textos processados."""

import re
import unicodedata

from src.token_tracker import contar_tokens


def extrair_campo(texto, rotulo):
    """Extrai um campo identificado por um rótulo no início da linha."""
    # Captura o conteúdo depois dos dois-pontos na linha do campo.
    correspondencia = re.search(
        rf"^\s*{rotulo}\s*:[ \t]*([^\r\n]+)",
        texto,
        re.I | re.M,
    )

    return correspondencia.group(1).strip() if correspondencia else None


def normalizar_texto(texto):
    """Converte para minúsculas e remove acentos."""
    # Separa os acentos das letras e remove apenas os acentos.
    return "".join(
        caractere
        for caractere in unicodedata.normalize("NFD", texto.lower())
        if unicodedata.category(caractere) != "Mn"
    )


def extrair_experiencia(texto):
    """Extrai experiência em anos ou meses."""
    valor_campo = extrair_campo(texto, r"experi[eê]ncia(?: profissional)?")

    # Aceita anos ou meses; sem unidade, considera anos.
    correspondencia = re.fullmatch(
        r"(\d+(?:[.,]\d+)?)\s*"
        r"(anos?|meses|m[eê]s)?"
        r"(?:\s+de experi[eê]ncia)?[.]?",
        valor_campo or "",
        re.I,
    )

    if not correspondencia:
        return None, valor_campo or "não informada"

    anos = float(correspondencia.group(1).replace(",", "."))
    unidade = (correspondencia.group(2) or "").lower()

    # Padroniza a experiência em anos para montar o parecer.
    if unidade.startswith("m"):
        anos /= 12

    descricao = f"{anos:g} anos".replace(".", ",")

    return anos, descricao


def gerar_parecer_simulado(texto):
    """Monta uma resposta personalizada usando regras didáticas."""
    nome = (
        extrair_campo(texto, r"nome(?: completo)?")
        or "Nome não informado"
    )

    pretensao_salarial = (
        extrair_campo(texto, r"pretens[aã]o salarial")
        or "não informada"
    )

    anos, experiencia = extrair_experiencia(texto)

    # A senioridade usa somente o tempo declarado como critério didático.
    if anos is None:
        senioridade = (
            "Não estimada: tempo de experiência ausente ou ambíguo."
        )
    else:
        if anos < 3:
            nivel = "Júnior"
        elif anos < 6:
            nivel = "Pleno"
        else:
            nivel = "Sênior"

        senioridade = (
            f"{nivel} "
            f"(estimativa didática por tempo declarado: {experiencia}). "
            "Critério da simulação: menos de 3 anos = Júnior; "
            "de 3 a menos de 6 = Pleno; a partir de 6 = Sênior. "
            "Confirmar complexidade dos projetos, autonomia "
            "e responsabilidades em entrevista."
        )

    # As palavras-chave apontam indícios, não comprovam habilidades.
    regras = {
        "Colaboração": (
            r"\b(colabor\w*|trabalho em equipe|"
            r"respeito mutuo|harmonia)\b"
        ),
        "Liderança": (
            r"\b(lider\w*|mentori\w*|coordenei|"
            r"coordeno|guiar|guiei)\b"
        ),
        "Comunicação": (
            r"\b(comunica\w*|apresentei|"
            r"apresentacoes|documentacao)\b"
        ),
    }

    # Divide o texto em trechos para indicar a origem de cada indício.
    trechos = [
        trecho.strip()
        for trecho in re.split(r"[\n.!?;]+", texto)
        if trecho.strip()
    ]

    indicios = []

    for habilidade, padrao in regras.items():
        for trecho in trechos:
            trecho_normalizado = normalizar_texto(trecho)

            # Ignora trechos com estas negações explícitas.
            if re.search(r"\b(nao|nunca|sem)\b", trecho_normalizado):
                continue

            if re.search(padrao, trecho_normalizado):
                indicios.append(
                    f'• {habilidade}: possível indício no trecho '
                    f'"{trecho}".'
                )
                # Usa apenas o primeiro trecho encontrado para cada habilidade.
                break

    if indicios:
        habilidades_comportamentais = "\n".join(indicios)
    else:
        habilidades_comportamentais = (
            "Não foram encontrados indícios suficientes "
            "nas regras desta simulação."
        )

    # Limita a identificação às tecnologias desta lista.
    tecnologias_reconhecidas = (
        "Python",
        "JavaScript",
        "TypeScript",
        "Java",
        "SQL",
        "React",
        "Docker",
        "AWS",
    )

    texto_normalizado = normalizar_texto(texto)
    tecnologias = []

    for tecnologia in tecnologias_reconhecidas:
        # Evita reconhecer Java dentro da palavra JavaScript, por exemplo.
        padrao = (
            r"(?<!\w)"
            + re.escape(tecnologia.lower())
            + r"(?!\w)"
        )

        if re.search(padrao, texto_normalizado):
            tecnologias.append(tecnologia)

    resumo_tecnologias = (
        ", ".join(tecnologias)
        if tecnologias
        else "nenhuma identificada no vocabulário da simulação"
    )

    # Monta o parecer e o resumo com os dados extraídos.
    resposta = (
        "--- PARECER QUALITATIVO E RESUMO EXECUTIVO "
        "(SIMULAÇÃO DIDÁTICA) ---\n\n"

        f"Candidato: {nome}\n"
        f"Pretensão salarial declarada: {pretensao_salarial}\n\n"

        "PARECER QUALITATIVO\n"
        f"Senioridade: {senioridade}\n\n"

        "Habilidades comportamentais — indícios a confirmar:\n"
        f"{habilidades_comportamentais}\n\n"

        "RESUMO EXECUTIVO PARA O RECRUTADOR\n"
        f"Apresentamos o perfil de {nome}. "
        f"Experiência declarada: {experiencia}. "
        f"Pretensão salarial declarada: {pretensao_salarial}. "
        f"Tecnologias mencionadas e reconhecidas: {resumo_tecnologias}.\n"

        f"Avaliação preliminar de senioridade: {senioridade}\n"

        "Aspectos comportamentais para aprofundar em entrevista:\n"
        f"{habilidades_comportamentais}\n\n"
    )

    return resposta


def analisar_curriculo(texto_curriculo):
    """Retorna análise simulada, tokens e estimativa de custo."""
    if not isinstance(texto_curriculo, str) or not texto_curriculo.strip():
        raise ValueError(
            "O currículo precisa conter texto para análise."
        )

    # O modelo serve de referência para tokens e preços; não há chamada de API.
    modelo = "gpt-4o-mini"

    # Define as instruções que compõem o texto de entrada da simulação.
    instrucoes_analise = (
        "Você é um assistente de triagem de currículos de tecnologia. "
        "Produza um parecer de senioridade e indícios de habilidades comportamentais, "
        "além de um resumo executivo personalizado. "
        "Não invente informações."
    )

    texto_entrada = (
        instrucoes_analise
        + "\n\n--- CURRÍCULO ---\n"
        + texto_curriculo
    )

    # Gera a resposta por regras locais.
    resposta = gerar_parecer_simulado(texto_curriculo)

    # Conta os textos completos de entrada e saída separadamente.
    tokens_entrada = contar_tokens(texto_entrada, modelo)
    tokens_saida = contar_tokens(resposta, modelo)

    total_tokens = tokens_entrada + tokens_saida

    # Tarifas em US$ por milhão de tokens, sem cache ou desconto de processamento em lote.
    tarifa_entrada = 0.15
    tarifa_saida = 0.60

    # Soma entrada e saída e converte a tarifa por milhão para esta execução.
    custo_estimado = (
        (tokens_entrada * tarifa_entrada)
        + (tokens_saida * tarifa_saida)
    ) / 1_000_000

    # Mantém seis casas decimais para mostrar custos menores que um centavo.
    relatorio_uso = {
        "modelo": modelo,
        "tokens_entrada": tokens_entrada,
        "tokens_saida": tokens_saida,
        "total_tokens": total_tokens,
        "custo_estimado": f"US$ {custo_estimado:.6f}",
    }

    return resposta, relatorio_uso
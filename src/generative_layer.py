import re
import unicodedata

from src.token_tracker import count_tokens


def field(text, label):
    """Extrai um campo identificado por um rótulo no início da linha."""
    match = re.search(
        rf"^\s*{label}\s*:[ \t]*([^\r\n]+)",
        text,
        re.I | re.M,
    )

    return match.group(1).strip() if match else None


def normalize(text):
    """Converte para minúsculas e remove acentos."""
    return "".join(
        char
        for char in unicodedata.normalize("NFD", text.lower())
        if unicodedata.category(char) != "Mn"
    )


def extract_experience(text):
    """Extrai experiência em anos ou meses."""
    raw = field(text, r"experi[eê]ncia(?: profissional)?")

    match = re.fullmatch(
        r"(\d+(?:[.,]\d+)?)\s*"
        r"(anos?|meses|m[eê]s)?"
        r"(?:\s+de experi[eê]ncia)?[.]?",
        raw or "",
        re.I,
    )

    if not match:
        return None, raw or "não informada"

    years = float(match.group(1).replace(",", "."))
    unit = (match.group(2) or "").lower()

    if unit.startswith("m"):
        years /= 12

    description = f"{years:g} anos".replace(".", ",")

    return years, description


def simulate_completion(text):
    """Monta uma resposta personalizada usando regras didáticas."""
    name = (
        field(text, r"nome(?: completo)?")
        or "Nome não informado"
    )

    salary = (
        field(text, r"pretens[aã]o salarial")
        or "não informada"
    )

    years, experience = extract_experience(text)

    if years is None:
        seniority = (
            "Não estimada: tempo de experiência ausente ou ambíguo."
        )
    else:
        if years < 3:
            level = "Júnior"
        elif years < 6:
            level = "Pleno"
        else:
            level = "Sênior"

        seniority = (
            f"{level} "
            f"(estimativa didática por tempo declarado: {experience}). "
            "Critério da simulação: menos de 3 anos = Júnior; "
            "de 3 a menos de 6 = Pleno; a partir de 6 = Sênior. "
            "Confirmar complexidade dos projetos, autonomia "
            "e responsabilidades em entrevista."
        )

    rules = {
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

    passages = [
        passage.strip()
        for passage in re.split(r"[\n.!?;]+", text)
        if passage.strip()
    ]

    evidence = []

    for skill, pattern in rules.items():
        for passage in passages:
            normalized = normalize(passage)

            if re.search(r"\b(nao|nunca|sem)\b", normalized):
                continue

            if re.search(pattern, normalized):
                evidence.append(
                    f'• {skill}: possível indício no trecho '
                    f'"{passage}".'
                )
                break

    if evidence:
        soft_skills = "\n".join(evidence)
    else:
        soft_skills = (
            "Não foram encontrados indícios suficientes "
            "nas regras desta simulação."
        )

    known_technologies = (
        "Python",
        "JavaScript",
        "TypeScript",
        "Java",
        "SQL",
        "React",
        "Docker",
        "AWS",
    )

    normalized_text = normalize(text)
    technologies = []

    for technology in known_technologies:
        pattern = (
            r"(?<!\w)"
            + re.escape(technology.lower())
            + r"(?!\w)"
        )

        if re.search(pattern, normalized_text):
            technologies.append(technology)

    tech_summary = (
        ", ".join(technologies)
        if technologies
        else "nenhuma identificada no vocabulário da simulação"
    )

    completion = (
        "--- PARECER QUALITATIVO E RESUMO EXECUTIVO "
        "(SIMULAÇÃO DIDÁTICA) ---\n\n"

        f"Candidato: {name}\n"
        f"Pretensão salarial declarada: {salary}\n\n"

        "PARECER QUALITATIVO\n"
        f"Senioridade: {seniority}\n\n"

        "Soft skills — indícios a confirmar:\n"
        f"{soft_skills}\n\n"

        "RESUMO EXECUTIVO PARA O RECRUTADOR\n"
        f"Apresentamos o perfil de {name}. "
        f"Experiência declarada: {experience}. "
        f"Pretensão salarial declarada: {salary}. "
        f"Tecnologias mencionadas e reconhecidas: {tech_summary}.\n"

        f"Avaliação preliminar de senioridade: {seniority}\n"

        "Aspectos comportamentais para aprofundar em entrevista:\n"
        f"{soft_skills}\n\n"
    )

    return completion


def candidate_profiler(file_content):
    """Retorna o parecer personalizado e o relatório de tokens."""
    if not isinstance(file_content, str) or not file_content.strip():
        raise ValueError(
            "O currículo precisa conter texto para análise."
        )

    model = "gpt-6-astra-sim"

    system_prompt = (
        "Você é um assistente de triagem de currículos de tecnologia. "
        "Produza um parecer de senioridade e indícios de soft skills, "
        "além de um resumo executivo personalizado. "
        "Não invente informações."
    )

    prompt = (
        system_prompt
        + "\n\n--- CURRÍCULO ---\n"
        + file_content
    )

    completion = simulate_completion(file_content)

    prompt_tokens = count_tokens(prompt, "gpt-6-astra-sim")
    completion_tokens = count_tokens(completion, "gpt-6-astra-sim")

    token_total = prompt_tokens + completion_tokens

    prompt_token_rate = 10
    completion_token_rate = 50

    cost = (((prompt_tokens * prompt_token_rate) + (completion_tokens * completion_token_rate)) / 1_000_000)
    clean_cost = f"US$ {cost:.6f}"

    token_report = {
        "model": model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "token_total": token_total,
        "cost": clean_cost
    }

    return completion, token_report
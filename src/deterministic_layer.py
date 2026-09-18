import re

from decimal import Decimal

def apply_filters(file_content, minimum_experience_years, budget):

    file_content_lower = file_content.lower()

    approved = True

    feedback = []

    # Part 1 - Experience

    experience_field = re.search(
        r"^[ \t]*experi[eê]ncia(?: profissional)?[ \t]*:"
        r"[ \t]*([^\r\n]+)",
        file_content_lower,
        flags=re.MULTILINE,
    )

    if experience_field is None:
        approved = False
        feedback.append(
            "Informação de experiência não encontrada no currículo.\n"
        )

    else:
        raw_experience = experience_field.group(1).strip()

        experience_pattern = (
            r"(\d+(?:[.,]\d+)?)"
            r"\s*"
            r"(anos?|meses|mês|mes)?"
            r"(?:\s+de\s+experiência)?"
            r"\.?"
        )

        experience_match = re.fullmatch(
            experience_pattern,
            raw_experience,
            flags=re.IGNORECASE,
        )

        if experience_match is None:
            approved = False
            feedback.append(
                f"Formato de experiência inválido: "
                f"{raw_experience!r}. "
                "Use, por exemplo, '28 anos' ou '18 meses'.\n"
            )

        else:
            experience_value = float(
                experience_match.group(1).replace(",", ".")
            )

            unit = (experience_match.group(2) or "anos").lower()

            if unit in ("meses", "mês", "mes"):
                extracted_experience = experience_value / 12
            else:
                extracted_experience = experience_value

            if extracted_experience < minimum_experience_years:
                approved = False
                feedback.append(
                    f"Experiência insuficiente: "
                    f"{extracted_experience:g} anos. "
                    f"Mínimo exigido: "
                    f"{minimum_experience_years:g} anos.\n"
                )

    # Part 2 - Budget

    target_budget_label = "pretensão salarial:"

    budget_pattern = (
        re.escape(target_budget_label)
        + r"\s*(?:r\$|\$)?\s*"
        + r"(\d{1,3}(?:\.\d{3})+|\d+)(?:,(\d{2}))?(?![\d.,])"
    )

    budget_match = re.search(budget_pattern, file_content_lower)

    if budget_match:
        integer_part = budget_match.group(1).replace(".", "")
        decimal_part = budget_match.group(2) or "00"

        expected_salary = Decimal(
            f"{integer_part}.{decimal_part}"
        )
        budget_value = Decimal(str(budget))

        if expected_salary > budget_value:
            approved = False
            feedback.append(
                f"Salary expectations ({expected_salary}) "
                f"exceed the budget ({budget_value}).\n"
            )
    else:
        approved = False
        feedback.append(
            "Salary expectation not found or invalid in the resume.\n"
        )

    return approved, feedback
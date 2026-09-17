import re

def apply_filters(file_content, minimum_experience_years, budget):

    file_content_lower = file_content.lower()

    approved = True

    feedback = []

    # Part 1 - Experience

    # Defina exatamente o que você quer buscar no texto antes do número
    target_experience_label = "experiência:" 

    # Usa o target_label no padrão, e procura no file_content_lower
    experience_pattern = rf"{re.escape(target_experience_label)}\s*(\d+(?:[.,]\d+)?)"
    experience_match = re.search(experience_pattern, file_content_lower)

    # Variável para armazenar o valor final da experiência
    extracted_experience = 0 

    if experience_match:
        # Pega o texto da regex (ex: "28")
        raw_str = experience_match.group(1).replace(',', '.')
        # Converte para int ou float
        extracted_experience = float(raw_str) if '.' in raw_str else int(raw_str)
    else:
        # Opcional: o que fazer se o currículo não tiver a palavra "Experiência:"
        approved = False
        feedback.append("Experience information not found in the resume.\n")

    # Agora a validação funciona, pois extracted_experience sempre existirá (sendo 28 ou 0)
    if extracted_experience < minimum_experience_years:
        approved = False
        feedback.append(f"More experience required: {extracted_experience} < {minimum_experience_years}\n")

   # Part 2 - Budget

    # 1. Define the label that comes right before the salary
    target_budget_label = "pretensão salarial:"

    # 2. Look for the label, an optional R$, and the number
    budget_pattern = rf"{re.escape(target_budget_label)}\s*(?:r\$|\$)?\s*(\d{1,3}(?:\.\d{3})*|\d+)"
    budget_match = re.search(budget_pattern, file_content_lower)

    if budget_match:
        # 3. Clean the captured number (e.g., "32.457" becomes "32457")
        clean_value = budget_match.group(1).replace('.', '')
        expected_salary = int(clean_value)
        
        # 4. FIX: Use '>' to check if the candidate's expectation EXCEEDS your budget
        if expected_salary > budget:
            approved = False
            feedback.append(f"Salary expectations ({expected_salary}) exceed the budget ({budget}).\n")
    else:
        approved = False
        feedback.append("Salary expectation not found in the resume.\n")

    return approved, feedback
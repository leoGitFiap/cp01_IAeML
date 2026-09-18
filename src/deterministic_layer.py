import re

from decimal import Decimal

def apply_filters(file_content, minimum_experience_years, budget):

    file_content_lower = file_content.lower()

    approved = True

    feedback = []

    # Part 1 - Experience

    target_experience_label = "experiência:" 

    experience_pattern = rf"{re.escape(target_experience_label)}\s*(\d+(?:[.,]\d+)?)"
    experience_match = re.search(experience_pattern, file_content_lower)

    extracted_experience = 0 

    if experience_match:
        raw_str = experience_match.group(1).replace(',', '.')
        extracted_experience = float(raw_str) if '.' in raw_str else int(raw_str)
    else:
        approved = False
        feedback.append("Experience information not found in the resume.\n")

    if (extracted_experience / 10) <= 1 :
        approved = False
        feedback.append(f"More experience required: {extracted_experience} < {minimum_experience_years}\n")

   # Part 2 - Budget

    target_budget_label = "pretensão salarial:"

    budget_pattern = (
        re.escape(target_budget_label)
        + r"\s*(?:r\$|\$)?\s*"
        + r"(\d{1,3}(?:\.\d{3})+|\d+)(?:,(\d{2}))?(?![\d.,])"
    )
    budget_match = re.search(budget_pattern, file_content_lower)

    if budget_match:
        clean_value = budget_match.group(1).replace('.', '')
        expected_salary = int(clean_value)
        
        if expected_salary > budget:
            approved = False
            feedback.append(f"Salary expectations ({expected_salary}) exceed the budget ({budget}).\n")
    else:
        approved = False
        feedback.append("Salary expectation not found in the resume.\n")

    return approved, feedback
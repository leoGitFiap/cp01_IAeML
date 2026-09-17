import re

def apply_filters(file_content, minimum_experience_years, budget):

    file_content_lower = file_content.lower()

    approved = True

    feedback = []

    # Part 1 - Experience

    experience_pattern = rf"{re.escape(file_content_lower)}\s*(\d+(?:[.,]\d+)?)"
    experience_match = re.search(experience_pattern, file_content_lower)

    if experience_match:
        raw_value = experience_match.group(1).replace(',', '.')
        return float(raw_value) if '.' in raw_value else int(raw_value)

    if raw_value < minimum_experience_years:
        approved = False
        feedback.append(f"More experience required: {raw_value} < {minimum_experience_years}\n")

    # Part 2 - Budget

    budget_pattern = r'(?:r\$|\$)?\s*(\d{1,3}(?:\.\d{3})*|\d+)'
    budget_match = re.findall(budget_pattern, file_content_lower)

    budget_match_found = []
    for v in budget_match:
        clean_value = v.replace('.', '')
        if clean_value.isdigit():
            budget_match_found.append(int(clean_value))

    if budget_match_found:
        min_value = min(budget_match_found)
        if min_value < budget:
            approved = False
            feedback.append(f"Salary expectations ({min_value}) exceed the budget ({budget}).\n")

    return approved, feedback
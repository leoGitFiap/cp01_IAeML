import re

def apply_filters(file_content, minimum_experience_years):

    file_content_lower = file_content.lower()

    approved = True

    feedback = []

    pattern = rf"{re.escape(file_content_lower)}\s*(\d+(?:[.,]\d+)?)"

    match = re.search(pattern, file_content_lower)

    if match:
        raw_value = match.group(1).replace(',', '.')
        return float(raw_value) if '.' in raw_value else int(raw_value)

    if raw_value < minimum_experience_years:
        approved = False
        feedback.append(f"More experience required: {raw_value} < {minimum_experience_years}")

    return approved, feedback
def is_valid_credit_card(card_number):
    # Remove hyphens to check for a continuous sequence of digits
    clean_card_number = card_number.replace("-", "")

    # Check if the length is exactly 16 digits
    if len(clean_card_number) != 16:
        return False

    # Check if all characters are digits
    if not clean_card_number.isdigit():
        return False

    # Check if the first digit is 4, 5, or 6
    if clean_card_number[0] not in '456':
        return False

    # Check for consecutive repeated digits (4 or more in a row)
    for i in range(13):  # Check until the 13th index to avoid out of range
        if clean_card_number[i] == clean_card_number[i + 1] == clean_card_number[i + 2] == clean_card_number[i + 3]:
            return False

    # Check if the format contains hyphens and if they are correctly placed
    if '-' in card_number:
        # The card number should have hyphens separating groups of 4 digits
        parts = card_number.split('-')
        if len(parts) != 4:
            return False
        for part in parts:
            if len(part) != 4:
                return False

    # If all checks passed, the card number is valid
    return True


# List of credit card numbers to check
credit_card_numbers = [
    "5123-4567-8912-3456",
    "61234-567-8912-3456",
    "4123356789123456",
    "5123-4567-8912-3456",
    "4444-4444-4444-4444"
]

# Validate each credit card number
for card_number in credit_card_numbers:
    if is_valid_credit_card(card_number):
        print(f"{card_number}: Valid")
    else:
        print(f"{card_number}: Invalid")
import re


def is_valid_email(email: str) -> bool:

    pattern = (
        r"^[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}$"
    )

    return bool(
        re.match(
            pattern,
            email
        )
    )


def is_valid_phone(phone: str) -> bool:

    digits = (
        phone.strip()
    )

    return (
        digits.isdigit()
        and len(digits) >= 10
        and len(digits) <= 15
    )


def is_valid_name(name: str) -> bool:

    return (
        len(name.strip()) >= 2
    )
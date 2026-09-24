# Reusable helper functions for input validation.

import re
from datetime import datetime

# Roll number check
VALID_ROLL_PATTERN = re.compile(r"^[A-Za-z0-9_\-/]{1,20}$")


def is_valid_roll_no(roll_no):
    # Roll no check
    if not roll_no:
        return False
    return bool(VALID_ROLL_PATTERN.match(roll_no))


def is_valid_name(name):
    # Naam khali na ho
    if not name or not name.strip():
        return False
    return any(ch.isalpha() for ch in name)


def is_valid_date(date_string):
    # Date sahi format mein hai ya nahi
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False
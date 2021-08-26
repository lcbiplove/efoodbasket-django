import re
from django.core.exceptions import ValidationError

def validate_fullname(fullname) -> None:
    if not re.search("/^[a-zA-Z ]+$/ ", fullname):
        raise ValidationError("Please enter a valid full name")

# def validate_contact(contact) -> None:
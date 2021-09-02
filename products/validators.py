import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_shop_name(value):
    if len(value) < 4:
        raise ValidationError(
            _('Please enter a valid shop name.'),
            code='invalid',
        )

def validate_address(address) -> None:
    if len(address) < 4:
        raise ValidationError(
            _('Please enter a valid address.'),
            code='invalid',
        )

def validate_contact(contact) -> None:
    if not re.search("^(\d{7}|\d{10})$", str(contact)):
        raise ValidationError(
            _('Please enter a valid contact number.'),
            code='invalid',
        )

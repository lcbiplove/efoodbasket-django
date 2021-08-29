import re
from .models import User, Trader
from django.core.validators import validate_email


# def validate_contact(contact) -> None:
class UserValidator():
    def __init__(self, data, names, *args, **kwargs) -> None:
        self.errors = {}
        """Validates user from the post method
        data: request.post
        names: array of name attributes
        """
        for key in data:
            if key in names:
                password = data['password'] if key == 'confpass' else None
                getattr(self, f"validate_{key}")(data[key], password)
        terms = data.get('terms', None)
        self.validate_terms(terms, None)

    def get_errors(self) -> dict:
        return self.errors

    def validate_fullname(self, fullname, extra) -> None:
        if not re.search("^[a-zA-Z]+(?:\s[a-zA-Z]+)+$", fullname):
            self.errors['fullname'] = "Please enter a valid full name."
        
    def validate_address(self, address, extra) -> None:
        if len(address) < 4:
            self.errors['address'] = "Please enter a valid address."

    def validate_contact(self, contact, extra) -> None:
        if not re.search("^(\d{7}|\d{10})$", contact):
            self.errors['contact'] = "Please enter a valid contact."
    
    def validate_email(self, email, extra) -> None:
        try:
            validate_email(email)
            if User.objects.filter(email=email).exists():
                self.errors['email'] = "Please enter another email. This email already exist."
        except Exception as e:
            self.errors['email'] = "Please enter a valid email address."
    
    def validate_terms(self, terms, extra) -> None:
        if not terms:
            self.errors['terms'] = "Please aggree with terms and conditions."
    
    def validate_password(self, password, extra) -> None:
        if not re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$", password):
            self.errors['password'] = "Please enter password with at least 8 letters containing uppercase, lowercase and digits."

    def validate_confpass(self, confpass, password) -> None:
        if password != confpass:
            self.errors['confpass'] = "Password does not match."


class TraderValidator(UserValidator):
    def validate_pan(self, pan, extra) -> None:
        if not re.search("[A-Z]{5}[0-9]{4}[A-Z]{1}", pan):
            self.errors['pan'] = "Please enter a valid pan number."
        elif Trader.objects.filter(pan=pan).exists():
            self.errors['pan'] = "Please enter another pan number. This already exist."
        
    def validate_type(self, type, extra) -> None:
        if len(type) < 4:
            self.errors['type'] = "Please enter a valid product type."
        elif Trader.objects.filter(product_type__icontains=type).exists():
            self.errors['type'] = "Please enter another product type."

    def validate_details(self, details, extra) -> None:
        if len(details) < 100:
            self.errors['details'] = "Please enter details of at least 100 characters"
    



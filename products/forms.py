from django import forms
from .models import Product

class CreateProductForm(forms.ModelForm):
    image = forms.ImageField(required=True)

    class Meta:
        model = Product
        fields = '__all__'

        error_messages = {
            'image': {
                'required': "Please choose at least one image.",
            },
        }
from django import forms
# from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from .models import Contact


class ContactForm(forms.ModelForm):
    """Форма подписки по email"""
    # captcha = ReCaptchaField()

    class Meta:
        model = Contact
        fields = ("email",)
        widgets = {
            "email": forms.TextInput(attrs={'type': "email", "class": "editContent", "placeholder": "Enter Your Email..."})
        }
        labels = {
            "email": ''
        }

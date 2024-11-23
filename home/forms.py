from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django_countries.fields import CountryField
from .models import Contact

class ContactForm(forms.ModelForm):
   class Meta:
      model = Contact
      fields = ('name', 'email', "country",'phone_number', 'subject','message')
      
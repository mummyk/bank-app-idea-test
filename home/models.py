from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    country = CountryField()
    phone_number = PhoneNumberField(null=True, blank=True)
    subject = models.CharField(max_length=500)
    message = models.TextField()
    replied = models.BooleanField("Reply", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
       return self.name
    
    class Meta:
          verbose_name = 'Contact Form'
          verbose_name_plural = 'Contact Forms'
          ordering = ['-created_at']
             
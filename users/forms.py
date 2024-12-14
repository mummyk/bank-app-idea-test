# forms.py


from allauth.account.forms import ChangePasswordForm
from allauth.account.forms import ResetPasswordForm
from allauth.account.forms import SignupForm
from allauth.account.forms import LoginForm
from django import forms
from django_countries.fields import CountryField
from .models import Profile
from phonenumber_field.formfields import PhoneNumberField
from .models import DomesticTransfer, LocalTransfer, InternationalTransfer


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        # Customize the username field
        self.fields['login'].widget = forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': 'Enter your email or username'
        })
        # Customize the password field
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': 'Enter your password'
        })


# forms.py


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        # Customize the email field
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': 'Enter your email'
        })
        # Customize the username field
      #   self.fields['username'].widget = forms.TextInput(attrs={
      #       'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
      #       'placeholder': 'Choose a username'
      #   })

        # Customize the password field
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': 'Confirm your password'
        })


# forms.py


class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)
        # Customize the email field
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': 'Enter your email to reset password'
        })


class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomChangePasswordForm, self).__init__(*args, **kwargs)
        # Customize the current password field
        self.fields['oldpassword'].widget = forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': 'Current Password'
        })
        # Customize the new password field
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': 'New Password'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': 'Confirm New Password'
        })


# forms.py


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='First Name',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-white shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
            'placeholder': 'Enter your first name'
        })
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Last Name',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-white shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
            'placeholder': 'Enter your last name'
        })
    )

    country = CountryField(blank_label='(select country)').formfield(
        widget=forms.Select(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
        })
    )
    phone_number = PhoneNumberField(required=True, widget=forms.TextInput(attrs={
        'class': 'block w-full rounded-md border-0 py-1.5 text-white shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
        'placeholder': 'Enter your Phone Number'
    }))

    class Meta:
        model = Profile
        fields = ['profile_picture', 'address', 'gender',
                  'phone_number', 'first_name', 'last_name', 'country']
        widgets = {
            'address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'block w-full rounded-md border-0 py-1.5 text-white shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
                'placeholder': 'Enter your address'
            }),
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], attrs={
                'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6'}),

            'phone_number': forms.TextInput(attrs={
                'class': 'block w-full rounded-md border-0 py-1.5 text-white shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
                'placeholder': 'Enter your phone number'
            }),
        }


class Profile_pictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']


class ProfileFormLite(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'Bonnie'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'Green'
    }))
    country = CountryField(blank_label='(select country)').formfield(
        widget=forms.Select(attrs={
            'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': 'United States'
        })
    )
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'e.g. San Francisco'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'e.g. California'
    }))

    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={
        'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'e.g. +(12)3456 789'
    }))
    birthday = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': '15/08/1990',
        'type': 'date'
    }))

    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': '123456'
    }))

    gender = forms.CharField(widget=forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], attrs={
        'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500'}),)

    class Meta:
        model = Profile
        # fields = ['first_name', 'last_name', "gender", 'country', 'city', 'address',
        #           'phone_number', 'birthday', 'zip_code']

        fields = ["gender", 'country', 'city', 'address',
                  'phone_number', 'birthday', 'zip_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].error_messages = {
                'required': '{} is required'.format(field.replace("_", " ").title())
            }


# Transfer fields

class DomesticTransferForm(forms.ModelForm):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=True,
        label="Amount",
        widget=forms.NumberInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
            'placeholder': 'Enter amount to transfer'
        })
    )

    beneficiary = forms.CharField(
        max_length=50,
        required=True,
        label="Beneficiary",
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
            'placeholder': 'Enter beneficiary name'
        })
    )

    password = forms.CharField(
        required=True,
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
            'placeholder': 'Enter your account password'
        })
    )

    class Meta:
        model = DomesticTransfer  # Replace with the desired transfer model
        fields = ['beneficiary', 'amount', 'password']


class LocalTransferForm(forms.ModelForm):
    beneficiary_bank = forms.CharField(
        max_length=50,
        required=True,
        label='Beneficiary Bank',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
            'placeholder': 'Enter the beneficiary bank name'
        })
    )

    beneficiary_account_number = forms.IntegerField(
        required=True,
        label='Beneficiary Account Number',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
            'placeholder': 'Enter beneficiary name'
        })
    )
    transaction_type = forms.ChoiceField(
        choices=LocalTransfer.TRANSACTION_TYPE,
        required=True,
        label='Transaction Type',
        widget=forms.Select(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6'
        })
    )
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=True,
        label='Amount',
        widget=forms.NumberInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
            'placeholder': 'Enter the transfer amount'
        })
    )
    password = forms.CharField(
        max_length=128,
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
            'placeholder': 'Enter your account password'
        })
    )

    class Meta:
        model = LocalTransfer
        fields = [
            'beneficiary_bank',
            'beneficiary_account_number',
            'transaction_type',
            'amount',
        ]


class InternationalTransferForm(forms.ModelForm):
    beneficiary_name = forms.CharField(
        max_length=50,
        required=True,
        label='Beneficiary Name',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
            'placeholder': 'Enter the beneficiary Full Name'
        })
    )

    beneficiary_account_number = forms.IntegerField(
        required=True,
        label='Beneficiary Account Number',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
            'placeholder': 'Enter beneficiary account number'
        })
    )
    transaction_type = forms.ChoiceField(
        choices=LocalTransfer.TRANSACTION_TYPE,
        required=True,
        label='Transaction Type',
        widget=forms.Select(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6'
        })
    )
    beneficiary_bank = forms.CharField(
        max_length=50,
        required=True,
        label='Beneficiary Bank',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
            'placeholder': 'Enter the beneficiary bank name'
        })
    )

    beneficiary_address = forms.CharField(
        required=True,
        label='Beneficiary Address',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
            'placeholder': 'Enter beneficiary address'
        })
    )
    country = CountryField(blank_label='(select country)').formfield(
        widget=forms.Select(attrs={
            'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': 'United States'
        })
    )
    routing_number = forms.CharField(
        required=True,
        label='Routing Number',
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
            'placeholder': 'Enter beneficiary routing number'
        })
    )
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=True,
        label='Amount',
        widget=forms.NumberInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
            'placeholder': 'Enter the transfer amount'
        })
    )
    password = forms.CharField(
        max_length=128,
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
            'placeholder': 'Enter your account password'
        })
    )

    class Meta:
        model = InternationalTransfer
        fields = [
            'beneficiary_name',
            'beneficiary_account_number',
            'transaction_type',
            'beneficiary_bank',
            'beneficiary_address',
            'country',
            'routing_number',
            'amount',
            'reason'
        ]
        widgets = {
            'reason': forms.Textarea(attrs={
                'rows': 3,
                'class': 'block w-full rounded-md border-0 py-1.5 text-white shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm p-3 sm:leading-6',
                'placeholder': 'Enter your Reason for the transaction'
            }), }

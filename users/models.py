import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db import transaction
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
import random
import string


def generate_unique_account_number():
    """Generate a unique 10-digit account number."""
    while True:
        account_number = int(''.join(random.choices(string.digits, k=10)))
        if not AccountNumber.objects.filter(account_number=account_number).exists():
            return account_number


class Profile(models.Model):
    """User profile fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True)
    country = CountryField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    gender = models.CharField(max_length=10)
    phone_number = PhoneNumberField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    updated = models.DateTimeField('Updated', auto_now=True)
    created = models.DateTimeField('Created', auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     # Generate account number if not already set
    #     if not self.account_number:
    #         self.account_number = generate_unique_account_number()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class AccountNumber(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="account_number")
    account_number = models.BigIntegerField(unique=True, blank=True, null=True)
    account_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'))
    account_type = models.CharField(max_length=50, default="online")
    account_currency = models.CharField(max_length=50, default="Dollar($)")
    password = models.CharField(
        max_length=128, null=True, blank=True)  # Hashed password field
    # New field to lock the account
    locked = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.account_number}'

    class Meta:
        verbose_name = 'Account Number'
        verbose_name_plural = 'Account Numbers'

    def clean(self):
        """Ensure balance is not negative"""
        if self.account_balance < 0:
            raise ValidationError("Wallet balance must be positive")

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = generate_unique_account_number()
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        """Set the wallet's password (hashed)"""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Check the wallet's password"""
        return check_password(raw_password, self.password)

    def lock_account(self):
        """Lock the account to prevent transactions"""
        self.locked = True
        self.save()

    def unlock_account(self):
        """Unlock the account to allow transactions"""
        self.locked = False
        self.save()

    # def deposit(self, amount):
    #     if self.locked:
    #         raise ValidationError(
    #             "This account is locked. Deposits are not allowed.")

    #     try:
    #         amount = Decimal(amount)

    #         if amount <= 0:
    #             raise ValidationError("Deposit amount must be positive")

    #         if self.account_balance + amount > Decimal('1000000000000.00'):
    #             raise ValidationError("Maximum Deposit limit reached")

    #         with transaction.atomic():
    #             self.account_balance += amount
    #             self.clean()
    #             self.save()

    #         return self.account_balance
    #     except ValidationError as e:
    #         print(f"Error during Deposit: {str(e)}")
    #         raise e

    # def withdraw(self, amount, password):
    #     if self.locked:
    #         raise ValidationError(
    #             "This account is locked. Withdrawals are not allowed.")

    #     try:
    #         amount = Decimal(amount)

    #         if amount <= 0:
    #             raise ValidationError("Withdraw amount must be positive")

    #         if amount > Decimal('10000.00'):
    #             raise ValidationError("Maximum withdrawal limit reached")

    #         if self.account_balance < amount:
    #             raise ValidationError("Insufficient balance to withdraw")

    #         if not check_password(password, self.password):
    #             raise ValidationError("Incorrect password.")

    #         with transaction.atomic():
    #             self.account_balance -= amount
    #             self.clean()
    #             self.save()

    #         return self.account_balance
    #     except ValidationError as e:
    #         print(f"Error during withdrawal: {str(e)}")
    #         raise e


class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('domestic_transfer', 'Domestic Transfer'),
        ('local_transfer', 'Local Transfer'),
        ('international_transfer', 'International Transfer'),
    ]
    STATUS = [
        ('in_process', 'IN_PROCESS'),
        ('completed', 'COMPLETED'),
        ('canceled', 'CANCELED'),
        ('in_review', 'IN_REVIEW'),
    ]

    wallet = models.ForeignKey(AccountNumber, on_delete=models.CASCADE)
    transaction_uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    transaction_type = models.CharField(
        max_length=50, choices=TRANSACTION_TYPE)
    incoming = models.CharField("Incoming", max_length=7, default='Credit')
    to_user = models.CharField(
        "beneficiary", max_length=50, default='0000000000')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=50, choices=STATUS, default='in_process')
    updated = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.wallet.locked:
            raise ValidationError(
                "Cannot perform transactions on a locked account.")

    def __str__(self):
        return f"{self.wallet.user.username}-{self.transaction_type} of {self.amount} on {self.timestamp}"


class DomesticTransfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beneficiary = models.CharField("beneficiary", max_length=50)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    updated = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.beneficiary} of {self.amount} on {self.timestamp}"

    def transfer(self, amount, password):
        # Access the user's account through the correct related name
        user_account = self.user.account_number

        if user_account.locked:
            raise ValidationError(
                "This account is locked. Transfers are not allowed."
            )

        try:
            amount = Decimal(amount)

            if amount <= 0:
                raise ValidationError("Transfer amount must be positive.")

            if amount < Decimal("1.00"):
                raise ValidationError("Amount must be greater than $1.00.")

            # Access the user's account balance through the correct related name
            user_account = self.user.account_number
            if user_account.account_balance < amount:
                raise ValidationError("Insufficient balance to transfer.")

            if not user_account.check_password(password):
                raise ValidationError("Incorrect password.")

            with transaction.atomic():
                user_account.account_balance -= amount  # Deduct balance
                user_account.save()  # Save updated account balance
                self.save()

            return user_account.account_balance
        except ValidationError as e:
            print(f"Error during transfer: {str(e)}")
            raise e


class LocalTransfer(models.Model):
    TRANSACTION_TYPE = [
        ('current', 'Current Account'),
        ('saving', 'Saving Account'),
        ('checking', 'Checking Account'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beneficiary_bank = models.CharField("beneficiary bank", max_length=50)
    beneficiary_account_number = models.BigIntegerField(blank=True, null=True)
    transaction_type = models.CharField(
        max_length=50, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    updated = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.beneficiary_bank} of {self.amount} on {self.timestamp}"

    def transfer(self, amount, password):
        # Access the user's account through the correct related name
        user_account = self.user.account_number

        if user_account.locked:
            raise ValidationError(
                "This account is locked. Transfers are not allowed."
            )

        try:
            amount = Decimal(amount)

            if amount <= 0:
                raise ValidationError("Transfer amount must be positive.")

            if amount < Decimal("1.00"):
                raise ValidationError("Amount must be greater than $1.00.")

            # Access the user's account balance through the correct related name
            user_account = self.user.account_number
            if user_account.account_balance < amount:
                raise ValidationError("Insufficient balance to transfer.")

            if not user_account.check_password(password):
                raise ValidationError("Incorrect password.")

            with transaction.atomic():
                user_account.account_balance -= amount  # Deduct balance
                user_account.save()  # Save updated account balance
                self.save()

            return user_account.account_balance
        except ValidationError as e:
            print(f"Error during transfer: {str(e)}")
            raise e


class InternationalTransfer(models.Model):
    TRANSACTION_TYPE = [
        ('current', 'Current Account'),
        ('saving', 'Saving Account'),
        ('checking', 'Checking Account'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beneficiary_name = models.CharField("beneficiary name", max_length=200)
    beneficiary_account_number = models.BigIntegerField(blank=True, null=True)
    transaction_type = models.CharField(
        max_length=50, choices=TRANSACTION_TYPE)
    beneficiary_bank = models.CharField("beneficiary bank", max_length=50)
    beneficiary_address = models.CharField(
        "beneficiary address", max_length=500)
    country = CountryField()
    routing_number = models.CharField("IBAN", max_length=500)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField("Reason", max_length=1500)
    updated = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.beneficiary_name} of {self.amount} on {self.timestamp}"

    def transfer(self, amount, password):
        # Access the user's account through the correct related name
        user_account = self.user.account_number

        if user_account.locked:
            raise ValidationError(
                "This account is locked. Transfers are not allowed."
            )

        try:
            amount = Decimal(amount)

            if amount <= 0:
                raise ValidationError("Transfer amount must be positive.")

            if amount < Decimal("1.00"):
                raise ValidationError("Amount must be greater than $1.00.")

            # Access the user's account balance through the correct related name
            user_account = self.user.account_number
            print(user_account.account_balance)
            if user_account.account_balance < amount:
                raise ValidationError("Insufficient balance to transfer.")

            if not user_account.check_password(password):
                raise ValidationError("Incorrect password.")

            with transaction.atomic():
                user_account.account_balance -= amount  # Deduct balance
                user_account.save()  # Save updated account balance
                self.save()

            return user_account.account_balance
        except ValidationError as e:
            print(f"Error during transfer: {str(e)}")
            raise e

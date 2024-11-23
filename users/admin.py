from django.contrib import admin

# Register your models here.
from .models import Profile, AccountNumber, Transaction, DomesticTransfer, LocalTransfer, InternationalTransfer


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "updated",
        "created",
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "wallet",
        "updated",
        "timestamp",
    )


@admin.register(DomesticTransfer)
class DomesticTransferAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "beneficiary",
        "updated",
        "timestamp",
    )


@admin.register(LocalTransfer)
class DLocalTransferAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "amount",
        "updated",
        "timestamp",
    )


@admin.register(InternationalTransfer)
class InternationalTransferAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "amount",
        "updated",
        "timestamp",
    )


@admin.action(description="Lock selected accounts")
def lock_selected_accounts(modeladmin, request, queryset):
    queryset.update(locked=True)


@admin.action(description="Unlock selected accounts")
def unlock_selected_accounts(modeladmin, request, queryset):
    queryset.update(locked=False)


class AccountNumberAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number',
                    'account_balance', 'locked', 'created')
    actions = [lock_selected_accounts, unlock_selected_accounts]


admin.site.register(AccountNumber, AccountNumberAdmin)

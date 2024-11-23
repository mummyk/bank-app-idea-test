import logging
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.apps import apps
from django.db import transaction
from .models import AccountNumber

logger = logging.getLogger(__name__)


@receiver(user_signed_up)
def assign_user_to_member_group(request, user, **kwargs):
    logger.info(f"Signal received: user_signed_up for user {user.username}")

    try:
        with transaction.atomic():
            # Generate and assign account number for the user
            account_number_obj, created = AccountNumber.objects.get_or_create(
                user=user)
            if created:
                logger.info(f"Account number {
                            account_number_obj.account_number} created for user {user.username}")

            # Create or get the 'Member' group
            group_name = "Member"
            member_group, created = Group.objects.get_or_create(
                name=group_name)

            # Assign permissions to the group
            for app in apps.get_app_configs():
                for model in app.get_models():
                    content_type = ContentType.objects.get_for_model(model)
                    for perm_code in ['view', 'add']:
                        codename = f'{perm_code}_{model._meta.model_name}'
                        permission = Permission.objects.filter(
                            content_type=content_type, codename=codename).first()
                        if permission:
                            member_group.permissions.add(permission)

            # Add the user to the 'Member' group
            user.groups.add(member_group)

            logger.info(f"User {user.username} added to 'Member' group with account number {
                        account_number_obj.account_number}")

    except Exception as e:
        logger.error(f"Error in assign_user_to_member_group for user {
                     user.username}: {str(e)}")

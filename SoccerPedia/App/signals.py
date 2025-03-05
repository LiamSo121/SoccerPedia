# In your app's signals.py
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from users.models import CustomUser  # Import CustomUser from the correct path


@receiver(pre_social_login)
def prevent_duplicate_user(sender, request, sociallogin, **kwargs):
    # Access the user data from the social account's extra_data
    email = sociallogin.account.extra_data.get('email')
    first_name = sociallogin.account.extra_data.get('given_name')  # 'given_name' is the field for the first name
    last_name = sociallogin.account.extra_data.get('family_name')  # 'family_name' is the field for the last name

    if email:
        try:
            # Check if a user with the same email already exists in CustomUser model
            existing_user = CustomUser.objects.get(email=email)
            if existing_user:
                # If a user exists, associate this social login with the existing user
                sociallogin.connect(request, existing_user)
                # Optionally, update the user's first name and last name
                existing_user.first_name = first_name
                existing_user.last_name = last_name
                existing_user.save()
        except ObjectDoesNotExist:
            # No existing user, proceed with regular flow
            pass

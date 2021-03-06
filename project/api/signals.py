# Django
# Third-Party
from auth0.v3.management import Auth0
from auth0.v3.management.rest import Auth0Error

from django.conf import settings
from django.db.models.signals import (
    post_save,
    pre_delete,
)
from django.dispatch import receiver

# Local
from .models import User
from .utils import get_auth0_token


@receiver(post_save, sender=User)
def user_post_save(sender, instance=None, created=False, raw=False, **kwargs):
    """Create Auth0 from user and send verification email."""
    if not raw:
        if created:
            if instance.person:
                token = get_auth0_token()
                auth0 = Auth0(
                    settings.AUTH0_DOMAIN,
                    token,
                )
                create_user_payload = {
                    "connection": "email",
                    "email": instance.email,
                    "email_verified": True,
                    "user_metadata": {
                        "name": instance.person.name
                    },
                    "app_metadata": {
                        "barberscore_id": str(instance.id),
                    }
                }
                try:
                    response = auth0.users.create(create_user_payload)
                except Auth0Error as e:
                    if 'The user already exists' in e.message:
                        return
                    else:
                        raise(e)
                instance.auth0_id = response['user_id']
                instance.save()


@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    if instance.auth0_id:
        token = get_auth0_token()
        auth0 = Auth0(
            settings.AUTH0_DOMAIN,
            token,
        )
        auth0.users.delete(instance.auth0_id)
    return

from django.contrib.contenttypes.models import ContentType

def create_user_profile(sender, **kwargs):
    """
    Create an empty Profile whenever a new User is created.
    """
    from minerva import models
    try:
        ContentType.objects.get_by_natural_key("minerva", "profile")
    except ContentType.DoesNotExist:
        # Minerva app hasn't been installed yet.
        return
    if not kwargs["created"]:
        return
    models.Profile(user=kwargs["instance"]).save()



def create_user_profile(sender, **kwargs):
    """
    Create an empty UserProfile whenever a new User is created.
    """
    from minerva import models
    if not kwargs["created"]:
        return
    models.UserProfile(student=kwargs["instance"]).save()


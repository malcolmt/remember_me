"""
Create initial Profile classes for any users in the system that don't
already have one.
"""

from django.contrib.auth import models as auth_models
from django.core.management import base

from minerva import models

class Command(base.BaseCommand):
    help = "Create Profiles for any Users that don't have one."

    def handle(self, *args, **options):
        if len(args):
            raise base.CommandError("Usage is create_user_profiles.")

        verbosity = int(options.get("verbosity", 0))
        for user in auth_models.User.objects.filter(profile=None):
            if verbosity > 0:
                print "Create profile for %s" % user
            models.Profile(user=user).save()

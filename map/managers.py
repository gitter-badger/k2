from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

class UserManager(models.GeoManager):
    """
    Custom manager for the Location model.
    """
    def get_query_set(self):
        """
        Overwrites the get_query_set to only return Locations for User.
        """
        user = ContentType.objects.get_for_model(User)
        return super(UserManager, self).get_query_set().filter(content_type=user)

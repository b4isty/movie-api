import uuid

from django.contrib.auth import get_user_model
from django.db import models


class Movie(models.Model):
    """
    Movie model which will be related to collection
    """
    uuid = models.UUIDField(unique=True, blank=False)
    title = models.CharField(max_length=250, blank=False, default='')
    description = models.TextField()
    # generes should be a choice field but not going there
    # otherwise have to search internet and find all the genres
    genres = models.CharField(max_length=30, blank=True, default='', db_index=True)

    def __str__(self):
        return self.title


class Collection(models.Model):
    """
    Collection model which contains collection infos
    """
    # not using as pk but it will work as pk as it's unique
    # uuid has some known issues when being used as pk
    user = models.ForeignKey(to=get_user_model(), related_name='collections',
                             on_delete=models.CASCADE, blank=False, null=True)
    collection_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, blank=True)
    title = models.CharField(max_length=250, blank=False, default='', db_index=True)
    description = models.TextField(blank=False, default='')
    movies = models.ManyToManyField(to=Movie, related_name='collections')

    def __str__(self):
        return self.title



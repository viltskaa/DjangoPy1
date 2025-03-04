from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=127)


class Book(models.Model):
    name = models.CharField(max_length=100)
    count_pages = models.IntegerField(default=0)

    author = models.ForeignKey(
        Author, on_delete=models.DO_NOTHING,
        null=True
    )

    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING,
    )

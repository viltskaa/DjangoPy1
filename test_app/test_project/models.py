from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self) -> str:
        return f"({self.pk}) {self.name}"


class Book(models.Model):
    name = models.CharField(max_length=100)
    count_pages = models.IntegerField(default=0)

    author = models.ForeignKey(
        Author, on_delete=models.DO_NOTHING,
        null=True
    )

    def __str__(self) -> str:
        if self.author is None:
            return f"({self.pk}) {self.name}"
        return f"({self.pk}) {self.name} author:{self.author.name}"

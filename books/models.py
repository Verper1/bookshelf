from django.db import models


class Book(models.Model):
    """Модель книги для БД."""
    title = models.CharField(max_length=512)
    author_full_name = models.CharField(max_length=512)
    year_of_publishing = models.SmallIntegerField()
    copies_printed = models.IntegerField()
    short_description = models.TextField()

    def __str__(self) -> str:
        return f"{self.title} ({self.author_full_name})"

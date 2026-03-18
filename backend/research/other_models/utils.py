from django.db import models

class YearCounter(models.Model):
    """
    A helper model for generating reference numbers for studies. Keeps a counter
    for each year, that get incremented when a new Study is created.
    """

    year = models.IntegerField(unique=True)
    counter = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.year}-{self.counter}"
from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    quantity = models.IntegerField()
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

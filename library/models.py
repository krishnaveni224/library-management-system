from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    quantity = models.IntegerField()
    is_borrowed = models.BooleanField(default=False)

    # New fields
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    borrow_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title


class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    book_title = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"
    
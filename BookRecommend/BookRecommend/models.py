# myapp/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    ISBN = models.CharField(max_length=13,unique=True)
    Book_Title = models.CharField(max_length=255)
    Book_Author = models.CharField(max_length=100)
    Year_Of_Publication = models.IntegerField()
    Publisher = models.CharField(max_length=100)
    Image_URL_S = models.URLField()
    Image_URL_M = models.URLField()
    Image_URL_L = models.URLField()
    bid = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'bx_book'

    def __str__(self):
        return self.Book_Title

class BookRating(models.Model):
    id = models.AutoField(primary_key=True)
    User_ID = models.IntegerField()
    ISBN = models.CharField(max_length=20)
    Book_Rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    class Meta:
        db_table = 'bx_bookrating'
    def __str__(self):
        return f"User: {self.User_ID}, ISBN: {self.ISBN}, Rating: {self.Book_Rating}"

class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'userhistory'

    def __str__(self):
        return f"{self.user.username} - {self.book.Book_Title}"


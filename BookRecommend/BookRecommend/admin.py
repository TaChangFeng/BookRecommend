# myapp/admin.py

from django.contrib import admin
from .models import Book, BookRating, UserHistory

# Register your models here.
admin.site.register(Book)
admin.site.register(BookRating)
admin.site.register(UserHistory)

from django.contrib import admin
from .models import Author, Category, Customer, Comment, Book

# Register your models here.

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Comment)
admin.site.register(Book)
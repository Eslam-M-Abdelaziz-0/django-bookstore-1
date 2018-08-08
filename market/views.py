from django.shortcuts import render
from .models import Book, Category

# Create your views here.

def index_page(request):
    return render(
        request,
        "market/index.html",
        dict(
            popular_books=Book.objects.all()[:5],
            categories=[Category.objects.all()[i::3] for i in range(3)]
        )
    )
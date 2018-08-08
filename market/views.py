from django.shortcuts import render, get_object_or_404
from .models import Book, Category, Comment

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

def product_page(request, pk):
    return render(
        request,
        "market/product.html",
        dict(
            book=get_object_or_404(Book, pk=pk)
        )
    )
import uuid
import difflib
import functools

from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from .models import Book, Category, ActivationLink
from .forms import FilterSearchForm, SignUpForm

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


def _compute_similarity_score(text1, text2, comp="difflib"):
    if comp == "basic":
        text1_set = {word.lower() for word in text1.split()}
        text2_set = {word.lower() for word in text2.split()}
        return len(text1_set & text2_set)
    else:
        return difflib.SequenceMatcher(None, text1, text2).ratio()


def search_page(request):
    books = None
    form = FilterSearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get("query")
        maxprice = form.cleaned_data.get("maxprice")
        category_pk = form.cleaned_data.get("category")
        sort = form.cleaned_data.get("sort")
        if category_pk:
            books = Book.objects.filter(categories__pk=category_pk) \
                                .filter(price__lte=maxprice)
        else:
            books = Book.objects.filter(price__lte=maxprice)

        books = list(books)
        if query:
            comp = functools.partial(_compute_similarity_score, query)
            books = [(book, comp(str(book).replace(",", "")))
                     for book in books]
            books.sort(key=lambda book_meta: book_meta[1], reverse=True)
            books = [book_meta[0] for book_meta in books if book_meta[1] > 0.1]

        if sort == "popularity":
            books.sort(key=lambda book: book.holders_count)
        elif sort == "score":
            books.sort(key=lambda book: book.score)

    else:
        raise Http404

    return render(request, "market/search.html", dict(
        books=books,
        form=form
    ))


def signup_page(request):
    if request.user.is_authenticated:
        raise Http404
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            confirm_link = ActivationLink.objects.create(
                user=user, link=str(uuid.uuid4())
            )
            confirm_link.save()
            user.email_user(
                "Инструкция по подтверждению аккаунта",
                render_to_string(
                    "market/account_confirm_email.html",
                    dict(
                        token=confirm_link.link,
                        domain=get_current_site(request).domain
                    )
                )
            )
            return redirect("confirm_done")
    else:
        form = SignUpForm()

    return render(request, "market/account_sign_up.html", dict(form=form))

def confirm_account(request, uuid):
    link = ActivationLink.objects.filter(link=str(uuid)).first()
    if link:
        user = link.user
        link.delete()
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("confirm_success")
        
    return redirect("/")
    
def confirm_success_page(request):
    return render(request, "market/account_confirm_success.html", dict())

def confirm_done_page(request):
    return render(request, "market/account_confirm_done.html", dict())

    
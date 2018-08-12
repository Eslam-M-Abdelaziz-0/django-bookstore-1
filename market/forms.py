from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Category


class FilterSearchForm(forms.Form):
    query = forms.CharField(
        min_length=2,
        max_length=360,
        required=False
    )
    sort = forms.ChoiceField(
        choices=(
            ("relevance", "По релевантности"),
            ("popularity", "По популярности"),
            ("reviews", "По отзывам"),
        ),
        label="Сортировка",
        initial="relevance",
        widget=forms.RadioSelect
    )
    maxprice = forms.IntegerField(
        label="Цена до",
        min_value=0,
        max_value=99999,
        initial=99999
    )
    category = forms.ChoiceField(
        choices=[
            (category.pk, category.name)
            for category in Category.objects.all()
        ],
        label="Категория книги",
        required=False
    )

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "email",
            "username", "password1", "password2",
        )


from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_page, name="index_page"),
    path("product/<int:pk>/", views.product_page, name="product_page"),
    path("search/", views.search_page, name="search")
]
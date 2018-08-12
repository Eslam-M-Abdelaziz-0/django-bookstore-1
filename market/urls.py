from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index_page, name="index_page"),
    path("product/<int:pk>/", views.product_page, name="product_page"),
    path("search/", views.search_page, name="search"),
    path("accounts/signup/", views.signup_page, name="signup_page"),
    path("accounts/confirm_done/", views.confirm_done_page, name="confirm_done"),
    path("accounts/confirm_success/", views.confirm_success_page, name="confirm_success"),
    path("accounts/confirm/<uuid:uuid>", views.confirm_account, name="confirm_account"),
    path("accounts/", include("django.contrib.auth.urls")),
]
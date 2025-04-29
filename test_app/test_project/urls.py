"""
URL configuration for test_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from . import books_view
from . import sign_up

auth = [
    path("accounts/signIn/", auth_views.LoginView.as_view()),
    path("accounts/logout/", auth_views.LogoutView.as_view()),
    path("accounts/signUp/", sign_up.signup),
]

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),
    # MY
    path('', books_view.get_books, name='index'),
    path('add', books_view.create_book, name='add_book'),
    path('profile', views.profile, name='profile'),
    path('edit', books_view.edit_book, name='edit_book'),
    path('delete', books_view.delete_book, name='delete_book'),
    path('add_to_basket', books_view.add_to_basket, name='add_to_basket'),
    path('basket', books_view.get_basket, name='basket'),
    path('minus_from_basket', books_view.minus_from_basket, name='minus_from_basket'),
    path('plus_to_basket', books_view.plus_to_basket, name='plus_to_basket'),
] + auth
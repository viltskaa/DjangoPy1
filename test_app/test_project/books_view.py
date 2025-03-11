from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render

from .models import Author, Book


def get_books(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()

    return render(request, 'books.html', {
        'books': books,
    })

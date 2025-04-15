from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render

from .models import Author, Book


def get_books(request: HttpRequest) -> HttpResponse:
    q = request.GET.get('q')
    pages = request.GET.get('pages')
    author = request.GET.get('author')

    result = ((Book.objects.filter(name__icontains=q)
               | Book.objects.filter(author__name__icontains=q))
              & Book.objects.filter(count_pages__gt=int(pages)))

    if author:
        result = result.difference(Book.objects.filter(author_id__exact=None))

    return render(request, 'books.html', {
        'books': result,
        'q': q,
        'pages': pages,
    })

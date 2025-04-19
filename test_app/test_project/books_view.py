from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import BookForm
from .models import Author, Book


def get_books(request: HttpRequest) -> HttpResponse:
    q = request.GET.get('q', "")
    pages = request.GET.get('pages', 0)
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


def create_book(request: HttpRequest) -> HttpResponse:
    if request.user is None or not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('/')

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            pages = form.cleaned_data['count_pages']
            author = form.cleaned_data['author']
            Book.objects.create(name=name, author=author, count_pages=pages)
            return redirect("/")
        else:
            return render(request, 'test.html', {
                'form': form,
                'errors': form.errors,
            })
    else:
        form = BookForm()
        return render(request, 'test.html', {
            'form': form,
        })


def edit_book(request: HttpRequest) -> HttpResponse:
    if request.user is None or not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('/')

    book_id = request.GET.get('book_id')
    book = Book.objects.get(id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            pages = form.cleaned_data['count_pages']
            author = form.cleaned_data['author']

            book.name = name
            book.count_pages = pages
            book.author = author
            book.save()

            return redirect("/")
        else:
            return render(request, 'test.html', {
                'form': form,
                'errors': form.errors,
            })
    else:
        form = BookForm()

        form.fields['name'].initial = book.name
        form.fields['count_pages'].initial = book.count_pages
        form.fields['author'].initial = book.author

        return render(request, 'test.html', {
            'form': form,
        })


def delete_book(request: HttpRequest) -> HttpResponse:
    book_id = request.GET.get('book_id')
    book = Book.objects.get(id=book_id)

    if request.method == 'POST':
        book.delete()
        return redirect("/")
    else:
        return render(request, 'delete_accept.html', {
            "name": book.name,
        })
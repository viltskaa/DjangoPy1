from dataclasses import dataclass

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, AbstractUser
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import BookForm
from .models import Author, Book, Basket


@dataclass
class BookDto:
    book: Book
    is_in_basket: bool
    count_in_basket: int


def get_books(request: HttpRequest) -> HttpResponse:
    q = request.GET.get('q', "")
    pages = request.GET.get('pages', 0)
    author = request.GET.get('author')

    result = ((Book.objects.filter(name__icontains=q)
               | Book.objects.filter(author__name__icontains=q))
              & Book.objects.filter(count_pages__gt=int(pages)))

    if author:
        result = result.difference(Book.objects.filter(author_id__exact=None))

    if request.user is None or not request.user.is_authenticated:
        return redirect('/')

    basket = Basket.objects.filter(user_id=request.user.id)

    books_dto = []

    for book in result:
        for item in basket:
            if item.product.pk == book.pk:
                book_dto = BookDto(
                    book=book,
                    is_in_basket=True,
                    count_in_basket=item.count,
                )
                books_dto.append(book_dto)
                break
        else:
            book_dto = BookDto(
                book=book,
                is_in_basket=False,
                count_in_basket=0,
            )
            books_dto.append(book_dto)

    return render(request, 'books.html', {
        'books': books_dto,
        'q': q,
        'pages': pages,
        'basket': basket,
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


def get_basket(request: HttpRequest) -> HttpResponse:
    if request.user is None or not request.user.is_authenticated:
        return redirect('/')

    basket = Basket.objects.filter(user_id=request.user.id)
    return render(request, 'basket.html', {
        "basket": basket,
    })


def add_to_basket(request: HttpRequest) -> HttpResponse:
    book_id = request.GET.get('book_id')
    book = Book.objects.get(id=book_id)

    if request.user is None or not request.user.is_authenticated:
        return redirect('/')

    user = request.user

    basket = Basket.objects.create(user=user, product=book, count=1)
    basket.save()

    return redirect("/")


def minus_from_basket(request: HttpRequest) -> HttpResponse:
    book_id = request.GET.get('product_id')
    book = Book.objects.get(id=book_id)

    update_count_in_basket(book, request.user, "-")
    return redirect("/")


def plus_to_basket(request: HttpRequest) -> HttpResponse:
    book_id = request.GET.get('product_id')
    book = Book.objects.get(id=book_id)

    update_count_in_basket(book, request.user, "+")
    return redirect("/")


def update_count_in_basket(product: Book, user: AbstractBaseUser, operation: str) -> int:
    basket_item = Basket.objects.get(user=user, product=product)
    if operation == '-':
        basket_item.count -= 1
        if basket_item.count == 0:
            basket_item.delete()
            return 0
    else:
        basket_item.count += 1

    basket_item.save()
    return basket_item.count

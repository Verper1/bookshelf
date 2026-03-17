from django.shortcuts import render

from books.crud.get_book import get_books, get_book


def index_view(request):
    return render(request, 'index.html')


def all_books_view(request):
    books = get_books()

    return render(request, 'all_books.html', context={'books': books})


def book_view(request, book_id: int):
    book = get_book(book_id=book_id)

    return render(request, 'book.html', context={'book': book})
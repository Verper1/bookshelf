"""Модуль для view, которые отдают страницы HTML с CSS или без него."""
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from books.crud.get_book import get_books, get_book


def index_view(request: HttpRequest) -> HttpResponse:
    """Отдача главной страницы."""
    return render(request, 'index.html')


def all_books_view(request: HttpRequest) -> HttpResponse:
    """Отдаёт все книги из БД."""
    books = get_books()

    return render(request, 'all_books.html', context={'books': books})


def book_view(request: HttpRequest, book_id: int) -> HttpResponse:
    """Отдаёт книгу по id из БД."""
    book = get_book(book_id=book_id)

    return render(request, 'book.html', context={'book': book})
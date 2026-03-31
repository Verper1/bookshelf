from django.shortcuts import render, get_object_or_404
from django.http import (HttpRequest, HttpResponse, JsonResponse,
                         HttpResponseNotFound, HttpResponseBadRequest,
                         HttpResponseNotAllowed)
from django.views.decorators.http import require_POST, require_GET
from .crud_db import get_books, create_book, delete_book, update_book, get_book
from .models import Book
from .views_utils import json_response, check_post_request


# ------------ json ответы ------------

@require_GET
def json_all_books_view(request: HttpRequest) -> JsonResponse:
    """Возвращает все книги из БД в виде формата json."""
    books = get_books()

    books_list = []

    for book in books:
        books_list.append(json_response(book))

    return JsonResponse(books_list, safe=False)

@require_GET
def json_book_view(request: HttpRequest, book_id:int) -> (
        JsonResponse | HttpResponseNotFound
):
    """Возвращает книгу id из БД в виде формата json."""
    book = get_object_or_404(Book, pk=book_id)

    return JsonResponse(json_response(book))

# ------------ Cтраницы HTML с CSS или без него ------------

@require_GET
def index_view(request: HttpRequest) -> HttpResponse:
    """Отдача главной страницы."""
    return render(request, 'index.html')

@require_GET
def all_books_view(request: HttpRequest) -> HttpResponse:
    """Отдаёт все книги из БД."""
    books = get_books()

    return render(request, 'all_books.html', context={'books': books})

@require_GET
def book_view(request: HttpRequest, book_id: int) -> HttpResponse:
    """Отдаёт книгу по id из БД."""
    book = get_object_or_404(Book, pk=book_id)

    return render(request, 'book.html', context={'book': book})

# ------------ Cоздание, обновление и удаление книги ------------

@require_POST
def create_book_view(request: HttpRequest) -> JsonResponse | HttpResponseBadRequest | HttpResponseNotAllowed:
    """Создаёт книгу в БД через POST запрос."""
    book = check_post_request(request=request, function=create_book)

    if isinstance(book, HttpResponseBadRequest):
        return book

    return JsonResponse(json_response(book=book))

@require_POST
def update_book_view(request: HttpRequest, book_id: int) -> (
        HttpResponse | HttpResponseBadRequest | JsonResponse
):
    """Обновляет книгу из БД по id через POST запрос."""
    if get_book(book_id=book_id) is None:
        return HttpResponseNotFound("Такой книги нет.")

    book = check_post_request(
        request=request,
        function=update_book,
        book_id=book_id
    )

    if isinstance(book, HttpResponseBadRequest):
        return book

    return JsonResponse(json_response(book=book))

@require_POST
def delete_book_view(request: HttpRequest, book_id: int) -> (
        HttpResponse | HttpResponseNotFound | HttpResponseNotAllowed
):
    """Удаление книги из БД по id через POST запрос."""
    if get_book(book_id=book_id) is None:
        return HttpResponseNotFound("Такой книги нет.")

    delete_book(book_id)

    return HttpResponse()

"""Модуль для view, которые отвечает создание, удаление и обновление книги."""
from django.http import (HttpRequest, HttpResponse, HttpResponseBadRequest,
                         JsonResponse,HttpResponseNotAllowed,
                         HttpResponseNotFound)
from django.views.decorators.csrf import csrf_exempt

from books.crud.get_book import get_book
from books.crud.create_book import create_book
from books.crud.delete_book import delete_book
from books.crud.update_book import update_book


@csrf_exempt
def create_book_view(request: HttpRequest) -> JsonResponse | HttpResponseBadRequest:
    """Создаёт книгу в БД через POST запрос."""
    title = request.POST.get("title")
    author_full_name = request.POST.get("author_full_name")
    year_of_publishing = request.POST.get("year_of_publishing")
    copies_printed = request.POST.get("copies_printed")
    short_description = request.POST.get("short_description")
    if not all([
        title,
        author_full_name,
        year_of_publishing,
        copies_printed,
        short_description
    ]):
        return HttpResponseBadRequest("One of required parameters are missing")

    book = create_book(
        title,
        author_full_name,
        year_of_publishing,
        copies_printed,
        short_description
    )

    return JsonResponse(
        {
            "id": book.pk,
            "title": book.title,
            "author_full_name": book.author_full_name,
            "year_of_publishing": book.year_of_publishing,
            "copies_printed": book.copies_printed,
            "short_description": book.short_description
        }
    )

@csrf_exempt
def delete_book_view(request: HttpRequest, book_id: int) -> (
        HttpResponse | HttpResponseNotFound | HttpResponseNotAllowed
):
    """Удаление книги из БД по id через POST запрос."""
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    book = get_book(book_id)

    if book is None:
        return HttpResponseNotFound()

    delete_book(book_id)

    return HttpResponse()

@csrf_exempt
def update_book_view(request: HttpRequest, book_id: int) -> (
        HttpResponse | HttpResponseBadRequest | JsonResponse
):
    """Удаляет книгу из БД по id через POST запрос."""
    title = request.POST.get("title")
    author_full_name = request.POST.get("author_full_name")
    year_of_publishing = request.POST.get("year_of_publishing")
    copies_printed = request.POST.get("copies_printed")
    short_description = request.POST.get("short_description")
    if not all([
        title,
        author_full_name,
        year_of_publishing,
        copies_printed,
        short_description
    ]):
        return HttpResponseBadRequest("One of required parameters are missing")

    book = update_book(
        book_id,
        title,
        author_full_name,
        year_of_publishing,
        copies_printed,
        short_description
    )

    return JsonResponse(
        {
            "id": book.pk,
            "title": book.title,
            "author_full_name": book.author_full_name,
            "year_of_publishing": book.year_of_publishing,
            "copies_printed": book.copies_printed,
            "short_description": book.short_description
        }
    )
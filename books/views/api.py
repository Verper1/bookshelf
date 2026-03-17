"""Модуль для view, которые отвечает за json ответы."""
from books.crud.get_book import get_books, get_book

from django.http import JsonResponse, HttpRequest, HttpResponseNotFound


def json_all_books_view(request: HttpRequest) -> JsonResponse:
    """Возвращает все книги из БД в виде формата json."""
    books = get_books()

    books_list = []

    for book in books:
        books_list.append(
            {
                "id": book.pk,
                "title": book.title,
                "author_full_name": book.author_full_name,
                "year_of_publishing": book.year_of_publishing,
                "copies_printed": book.copies_printed,
                "short_description": book.short_description
            }
        )

    return JsonResponse(books_list, safe=False)

def json_book_view(request: HttpRequest, book_id:int) -> (
        JsonResponse | HttpResponseNotFound
):
    """Возвращает книгу id из БД в виде формата json."""
    book = get_book(book_id=book_id)

    if not book:
        return HttpResponseNotFound()

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

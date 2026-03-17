from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed

from books.models import Book
from .get_book import get_book


def delete_book(book_id: int) -> None:
    """Удаляет запись книги в БД по id или отдаёт ответ Not Found."""
    request_get = Book.objects.get(id=book_id)
    request_get.delete()


def delete_book_handler(request: HttpRequest, book_id: int) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    book = get_book(book_id)

    if book is None:
        return HttpResponseNotFound()

    delete_book(book_id)

    return HttpResponse()
# from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseNotFound

from books.models import Book
from django.db.models import QuerySet


def get_book(book_id: int) -> Book | None:
    """Получает запись книги со всеми полями по id или отдаёт ответ Not Found."""
    try:
        return Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return None


def get_books()-> QuerySet[Book]:
    """Получает записи книг со всеми полями по id или отдаёт ответ Not Found."""
    return Book.objects.all()


# def book_details_handler(request: HttpRequest, book_id: int) -> HttpResponse:
#     book = get_book(book_id)
#
#     if book is None:
#         return HttpResponseNotFound()
#
    # return JsonResponse(
    #     {
    #         "id": book.pk,
    #         "title": book.title,
    #         "author_full_name": book.author_full_name,
    #         "year_of_publishing": book.year_of_publishing,
    #         "copies_printed": book.copies_printed,
    #         "short_description": book.short_description
    #     }
    # )


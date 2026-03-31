from typing import Callable

from books.models import Book
from django.http import HttpRequest, HttpResponseBadRequest

required_fields = [
    "title",
    "author_full_name",
    "year_of_publishing",
    "copies_printed",
    "short_description",
]

def json_response(book: Book) -> dict:
    json_data = {
        "id": book.pk,
        "title": book.title,
        "author_full_name": book.author_full_name,
        "year_of_publishing": book.year_of_publishing,
        "copies_printed": book.copies_printed,
        "short_description": book.short_description
    }

    return json_data


def check_post_request(request: HttpRequest, function: Callable, book_id: int = None) -> (
        Book | HttpResponseBadRequest
):
    for field in required_fields:
        if field not in request.POST or not request.POST[field]:
            return HttpResponseBadRequest(f"Пропущенное поле: {field}")

    try:
        year_of_publishing = int(request.POST["year_of_publishing"])
        copies_printed = int(request.POST["copies_printed"])
    except ValueError:
        return HttpResponseBadRequest("year_of_publishing и copies_printed должны быть целочисленными.")
    if book_id:
        book = function(
            book_id,
            request.POST["title"],
            request.POST["author_full_name"],
            year_of_publishing,
            copies_printed,
            request.POST["short_description"]
        )
    else:
        book = function(
            request.POST["title"],
            request.POST["author_full_name"],
            year_of_publishing,
            copies_printed,
            request.POST["short_description"]
        )

    return book

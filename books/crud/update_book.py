from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse

from books.models import Book

def update_book(
        book_id: int,
        title: str,
        author_full_name: str,
        year_of_publishing: int,
        copies_printed: int,
        short_description: str) -> Book | None:
    """Обновляет поля книги по введённым значениям и id или отдаёт ответ Bad Request."""
    updated = Book.objects.filter(id=book_id).update(
        title=title,
        author_full_name=author_full_name,
        year_of_publishing=year_of_publishing,
        copies_printed=copies_printed,
        short_description=short_description
    )

    if updated == 0:
        return None

    return Book.objects.get(id=book_id)


def update_book_handler(request: HttpRequest, book_id: int) -> HttpResponse:
    title = request.POST.get("title")
    author_full_name = request.POST.get("author_full_name")
    year_of_publishing = int(request.POST.get("year_of_publishing"))
    copies_printed = int(request.POST.get("copies_printed"))
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

    if book is None:
        return HttpResponseBadRequest()

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
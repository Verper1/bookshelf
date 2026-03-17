from books.models import Book
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse


def create_book(title: str,
                author_full_name: str,
                year_of_publishing: int,
                copies_printed: int,
                short_description: str) -> Book:
    """Создаёт запись в БД с введёнными полями."""
    return Book.objects.create(title=title,
                               author_full_name=author_full_name,
                               year_of_publishing=year_of_publishing,
                               copies_printed=copies_printed,
                               short_description=short_description)


def create_book_handler(request: HttpRequest) -> HttpResponse:
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
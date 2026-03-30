from django.shortcuts import render, get_object_or_404
from django.http import (HttpRequest, HttpResponse, JsonResponse,
                         HttpResponseNotFound, HttpResponseBadRequest,
                         HttpResponseNotAllowed)
from .crud_db import get_books, create_book, delete_book, update_book
from .models import Book


# ------------ json ответы ------------

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

def json_all_books_view(request: HttpRequest) -> JsonResponse:
    """Возвращает все книги из БД в виде формата json."""
    books = get_books()

    books_list = []

    for book in books:
        books_list.append(json_response(book))

    return JsonResponse(books_list, safe=False)

def json_book_view(request: HttpRequest, book_id:int) -> (
        JsonResponse | HttpResponseNotFound
):
    """Возвращает книгу id из БД в виде формата json."""
    book = get_object_or_404(Book, pk=book_id)

    return JsonResponse(json_response(book))

# ------------ Cтраницы HTML с CSS или без него ------------

def index_view(request: HttpRequest) -> HttpResponse:
    """Отдача главной страницы."""
    contex =[

    ]
    return render(request, 'index.html')


def all_books_view(request: HttpRequest) -> HttpResponse:
    """Отдаёт все книги из БД."""
    books = get_books()

    return render(request, 'all_books.html', context={'books': books})


def book_view(request: HttpRequest, book_id: int) -> HttpResponse:
    """Отдаёт книгу по id из БД."""
    book = get_object_or_404(Book, pk=book_id)

    return render(request, 'book.html', context={'book': book})

# ------------ Cоздание, удаление и обновление книги ------------

def create_book_view(request: HttpRequest) -> JsonResponse | HttpResponseBadRequest | HttpResponseNotAllowed:
    """Создаёт книгу в БД через POST запрос."""
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    required_fields = [
        "title",
        "author_full_name",
        "year_of_publishing",
        "copies_printed",
        "short_description",
    ]

    # Проверка обязательных параметров
    for field in required_fields:
        if field not in request.POST or not request.POST[field]:
            return HttpResponseBadRequest(f"Пропущенное поле: {field}")

    # Приведение типов
    try:
        year_of_publishing = int(request.POST["year_of_publishing"])
        copies_printed = int(request.POST["copies_printed"])
    except ValueError:
        return HttpResponseBadRequest("year_of_publishing и copies_printed должны быть целочисленными.")

    if not all([
        request.POST["title"],
        request.POST["author_full_name"],
        year_of_publishing,
        copies_printed,
        request.POST["short_description"]
    ]):
        return HttpResponseBadRequest("One of required parameters are missing")

    book = create_book(
        request.POST["title"],
        request.POST["author_full_name"],
        year_of_publishing,
        copies_printed,
        request.POST["short_description"]
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

def delete_book_view(request: HttpRequest, book_id: int) -> (
        HttpResponse | HttpResponseNotFound | HttpResponseNotAllowed
):
    """Удаление книги из БД по id через POST запрос."""
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    book = get_object_or_404(Book, pk=book_id)

    delete_book(book_id)

    return HttpResponse()


def update_book_view(request: HttpRequest, book_id: int) -> (
        HttpResponse | HttpResponseBadRequest | JsonResponse
):
    """Обновляет книгу из БД по id через POST запрос."""
    if request.method != "POST":
        return HttpResponseBadRequest("POST метод ожидается.")

    required_fields = [
        "title",
        "author_full_name",
        "year_of_publishing",
        "copies_printed",
        "short_description",
    ]

    # Проверка обязательных параметров
    for field in required_fields:
        if field not in request.POST or not request.POST[field]:
            return HttpResponseBadRequest(f"Пропущенное поле: {field}")

    # Приведение типов
    try:
        year_of_publishing = int(request.POST["year_of_publishing"])
        copies_printed = int(request.POST["copies_printed"])
    except ValueError:
        return HttpResponseBadRequest("year_of_publishing и copies_printed должны быть целочисленными.")

    book = get_object_or_404(Book, pk=book_id)

    book = update_book(
        book_id,
        request.POST["title"],
        request.POST["author_full_name"],
        year_of_publishing,
        copies_printed,
        request.POST["short_description"]
    )

    if not book:
        return HttpResponseBadRequest("Не получилось обновить книгу.")
    else:
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

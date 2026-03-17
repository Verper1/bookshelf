from books.crud.get_book import get_books, get_book

from django.http import JsonResponse


def json_all_books_view(request):
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

def json_book_view(request, book_id:int):
    book = get_book(book_id=book_id)

    if not book:
        return JsonResponse({})

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

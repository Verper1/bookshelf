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

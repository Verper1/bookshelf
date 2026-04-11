from books.models import Book
from django.db.models import QuerySet


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


def get_book(book_id: int) -> Book | None:
    """Получает запись книги со всеми полями по id или отдаёт ответ Not Found."""
    try:
        return Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return None


def get_books()-> QuerySet[Book]:
    """Получает записи книг со всеми полями по id или отдаёт ответ Not Found."""
    return Book.objects.all()


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


def delete_book(book_id: int) -> None:
    """Удаляет запись книги в БД по id или отдаёт ответ Not Found."""
    request_get = Book.objects.get(id=book_id)
    request_get.delete()
from books.models import Book


def delete_book(book_id: int) -> None:
    """Удаляет запись книги в БД по id или отдаёт ответ Not Found."""
    request_get = Book.objects.get(id=book_id)
    request_get.delete()
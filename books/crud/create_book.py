from books.models import Book


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

import pytest
from django.urls import reverse
from books.models import Book


class FakeBook:
    def __init__(self, pk, title, author_full_name, year, copies, desc):
        self.pk = pk
        self.id = pk
        self.title = title
        self.author_full_name = author_full_name
        self.year_of_publishing = year
        self.copies_printed = copies
        self.short_description = desc

@pytest.mark.django_db
def test__all_books__integration_test(client):
    Book.objects.create(
        title="Book 1", author_full_name="Author 1", year_of_publishing=2000,
        copies_printed=10, short_description="Desc 1"
    )
    Book.objects.create(
        title="Book 2", author_full_name="Author 2", year_of_publishing=2010,
        copies_printed=5, short_description="Desc 2"
    )

    url = reverse('all_books')
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert "Book 1" in content
    assert "Author 1" in content
    assert "Book 2" in content
    assert "Author 2" in content


@pytest.mark.django_db
def test__book__integration_test_book_exists(client):
    book = Book.objects.create(
        title="Book 1", author_full_name="Author 1", year_of_publishing=2000,
        copies_printed=10, short_description="Desc 1"
    )

    url = reverse('book', kwargs={'book_id': book.id})
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert "Book 1" in content
    assert "Author 1" in content
    assert "2000" in content


@pytest.mark.django_db
def test__all_books__mock_test(client, mocker):
    book1 = FakeBook(1, "Book 1", "Author 1", 2000, 10, "Desc 1")
    book2 = FakeBook(2, "Book 2", "Author 2", 2010, 5, "Desc 2")

    mocker.patch('books.views.get_books',
                 return_value=[book1, book2])

    url = reverse('all_books')
    response = client.get(url)

    content = response.content.decode()
    assert "Book 1" in content
    assert "Book 2" in content


@pytest.mark.django_db
def test__book__mock_test_book_exists(client, mocker):
    book1 = FakeBook(
        1,
        "Book 1",
        "Author 1",
        2000,
        10,
        "Desc 1"
    )

    mocker.patch('books.views.get_object_or_404', return_value=book1)

    url = reverse('book', kwargs={'book_id': 1})
    response = client.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert "Book 1" in content
    assert "Author 1" in content
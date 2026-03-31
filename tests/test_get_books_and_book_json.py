from unittest.mock import MagicMock

import pytest
from django.urls import reverse
from books.models import Book
from django.test import Client

@pytest.mark.django_db
def test__json_all_books__integration_test(client: Client):
    Book.objects.create(
        title="Book 1",
        author_full_name="Author 1",
        year_of_publishing=2000,
        copies_printed=10,
        short_description="Desc 1"
    )
    Book.objects.create(
        title="Book 2",
        author_full_name="Author 2",
        year_of_publishing=2010,
        copies_printed=5,
        short_description="Desc 2"
    )

    url = reverse('json_all_books')
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]['title'] == "Book 1"
    assert data[1]['title'] == "Book 2"


@pytest.mark.django_db
def test__json_book__integration_test_book_exists(client: Client):
    book = Book.objects.create(
        title="Book 1",
        author_full_name="Author 1",
        year_of_publishing=2000,
        copies_printed=10,
        short_description="Desc 1"
    )

    url = reverse('json_book', kwargs={'book_id': book.id})
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "Book 1"
    assert data['author_full_name'] == "Author 1"


@pytest.mark.django_db
def test__json_book__integration_test_book_does_not_exists(client: Client):
    url = reverse('json_book', kwargs={'book_id': 999})
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test__json_all_books__mock_test(client: Client, mocker):
    book1 = MagicMock(pk=1, title="Book 1", author_full_name="Author 1",
                      year_of_publishing=2000, copies_printed=10, short_description="Desc 1")
    book2 = MagicMock(pk=2, title="Book 2", author_full_name="Author 2",
                      year_of_publishing=2010, copies_printed=5, short_description="Desc 2")

    # Патчим именно то, что view вызывает
    mocker.patch('books.views.get_books', return_value=[book1, book2])

    url = reverse('json_all_books')
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]['title'] == "Book 1"
    assert data[1]['title'] == "Book 2"


@pytest.mark.django_db
def test__json_book__mock_test_book_exists(client: Client, mocker):
    book = MagicMock(
        pk=1,
        title="Book 1",
        author_full_name="Author 1",
        year_of_publishing=2000,
        copies_printed=10,
        short_description="Desc 1"
    )

    mocker.patch('books.views.get_object_or_404', return_value=book)

    url = reverse('json_book', kwargs={'book_id': 1})
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "Book 1"
    assert data['author_full_name'] == "Author 1"


@pytest.mark.django_db
def test__json_book__mock_test_book_does_not_exists(client: Client, mocker):
    from django.http import Http404
    mocker.patch('books.views.get_object_or_404', side_effect=Http404)

    url = reverse('json_book', kwargs={'book_id': 999})
    response = client.get(url)

    assert response.status_code == 404

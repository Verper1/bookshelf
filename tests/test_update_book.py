import pytest
from django.urls import reverse
from books.models import Book
from unittest.mock import MagicMock

@pytest.mark.django_db
def test__update__integration_test_update_book(client):
    book = Book.objects.create(
        title="Old Title",
        author_full_name="Old Author",
        year_of_publishing=2000,
        copies_printed=5,
        short_description="Old description"
    )

    url = reverse('update', kwargs={'book_id': book.id})

    data = {
        'title': 'New Title',
        'author_full_name': 'New Author',
        'year_of_publishing': 2024,
        'copies_printed': 10,
        'short_description': 'New description'
    }

    response = client.post(url, data)

    assert response.status_code == 200
    content = response.json()
    assert content['title'] == 'New Title'
    assert content['author_full_name'] == 'New Author'

    book.refresh_from_db()
    assert book.title == 'New Title'
    assert book.author_full_name == 'New Author'
    assert book.year_of_publishing == 2024


def test__update__mock_test_update_book(client, mocker):
    book = MagicMock()
    book.pk = 1
    book.title = "New Title"
    book.author_full_name = "New Author"
    book.year_of_publishing = 2024
    book.copies_printed = 10
    book.short_description = "New description"

    mocker.patch('books.views.update_book', return_value=book)

    url = reverse('update', kwargs={'book_id': 1})

    data = {
        'title': 'New Title',
        'author_full_name': 'New Author',
        'year_of_publishing': 2024,
        'copies_printed': 10,
        'short_description': 'New description'
    }

    response = client.post(url, data)

    assert response.status_code == 200
    content = response.json()
    assert content['title'] == 'New Title'
    assert content['author_full_name'] == 'New Author'
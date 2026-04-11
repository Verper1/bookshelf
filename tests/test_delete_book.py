from books.models import Book
import pytest
from django.urls import reverse
from django.test import Client
from unittest.mock import MagicMock

@pytest.mark.django_db
def test__delete__integration_test_delete_book(client: Client):
    book = Book.objects.create(
        title="Book to Delete",
        author_full_name="Author",
        year_of_publishing=2000,
        copies_printed=5,
        short_description="Desc"
    )

    url = reverse('delete', kwargs={'book_id': book.id})

    response = client.post(url)

    assert response.status_code == 200

    assert Book.objects.filter(id=book.id).count() == 0

    response_get = client.get(url)
    assert response_get.status_code == 405

    response_not_found = client.post(reverse('delete', kwargs={'book_id': 9999}))
    assert response_not_found.status_code == 404


@pytest.mark.django_db
def test__delete__mock_test_delete_book(client: Client, mocker):
    fake_book = MagicMock()
    mocker.patch('books.views.get_book', return_value=fake_book)
    mock_delete = mocker.patch('books.views.delete_book')

    url = reverse('delete', kwargs={'book_id': 1})
    response = client.post(url)

    assert response.status_code == 200
    mock_delete.assert_called_once_with(1)

    response_get = client.get(url)
    assert response_get.status_code == 405
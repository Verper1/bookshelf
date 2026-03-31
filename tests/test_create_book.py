import pytest
from books.models import Book
from django.urls import reverse
from django.test import Client

@pytest.mark.django_db  # integration тест
def test__create_book__integration_test(client: Client):
    data = {
        'title': 'Test',
        'author_full_name': 'Author',
        'year_of_publishing': 2020,
        'copies_printed': 10,
        'short_description': 'desc'
    }

    url = reverse('create')
    response = client.post(url, data)

    assert response.status_code == 200
    assert Book.objects.count() == 1

@pytest.mark.django_db
def test__create_book__mock_test(mocker, client: Client):  # mock тест
    mock_create = mocker.patch('books.views.create_book')
    mock_create.return_value.pk = 1
    mock_create.return_value.title = 'Test Book'
    mock_create.return_value.author_full_name = 'Author Full Name'
    mock_create.return_value.year_of_publishing = 2222
    mock_create.return_value.copies_printed = 21
    mock_create.return_value.short_description = 'Short description'

    data = {
        'title': 'Test Book',
        'author_full_name': 'Author Full Name',
        'year_of_publishing': 2222,
        'copies_printed': 21,
        'short_description': 'Short description'
    }

    response = client.post(reverse('create'), data)
    mock_create.assert_called_once()

    assert response.status_code == 200
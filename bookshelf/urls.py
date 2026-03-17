"""Модуль для маршрутизации."""
from django.contrib import admin
from django.urls import path
from books.views.pages import index_view, all_books_view, book_view

from books.views.api import json_all_books_view, json_book_view

from books.views.crud import create_book_view, update_book_view, \
    delete_book_view

urlpatterns = [
    path('', index_view),
    path('admin/', admin.site.urls),
    path('books/', all_books_view, name='all_books'),
    path('books/<int:book_id>/', book_view, name='book'),
    path('api/books/', json_all_books_view, name='json_all_books'),
    path('api/books/<int:book_id>/', json_book_view, name='json_book'),
    path('api/book/create/', create_book_view, name='create'),
    path('api/book/<int:book_id>/update/', update_book_view, name='update'),
    path('api/book/<int:book_id>/delete/', delete_book_view, name='delete'),
]

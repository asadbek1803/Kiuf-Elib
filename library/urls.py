from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.books_list, name='books_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/save/', views.save_book, name='save_book'),
    path('books/<int:pk>/unsave/', views.unsave_book, name='unsave_book'),
    path('books/<int:pk>/download/', views.download_book, name='download_book'),
    path('books/<int:pk>/rate/', views.rate_book, name='rate_book'),
    path('saved/', views.saved_books, name='saved_books'),
    path('history/', views.reading_history, name='reading_history'),
    path('search/', views.search, name='search'),
    path('admin-help/', views.admin_help, name='admin_help'),
]

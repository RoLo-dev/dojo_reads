from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    path('', views.index, name='index'),
    path('books', views.books, name='books'),
    path('books/add', views.add_book, name='add_book'),
    path('books/add/validate', views.add_validate, name='add_validate'),
    path('books/<int:>', views.book_info, name='book_info'),
    path('users/<int:>', views.users_profile, name='users_profile'),

    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout')
]
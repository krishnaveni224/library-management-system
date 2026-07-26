from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='home'),

    path('books/', views.books, name='books'),
    path('add-book/', views.add_book, name='add_book'),
    path('edit-book/<int:id>/', views.edit_book, name='edit_book'),
    path('delete-book/<int:id>/', views.delete_book, name='delete_book'),

    path('borrow-book/<int:id>/', views.borrow_book, name='borrow_book'),
    path('return-book/<int:id>/', views.return_book, name='return_book'),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_user, name='logout'),
]

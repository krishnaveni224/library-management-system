from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Book
from .forms import BookForm

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required


@login_required
def books(request):

    search = request.GET.get('search', '')

    if search:

        books = Book.objects.filter(
            Q(title__icontains=search) |
            Q(author__icontains=search) |
            Q(genre__icontains=search)
        )

    else:

        books = Book.objects.all()

    return render(request, 'books.html', {
        'books': books,
        'search': search
    })


@login_required
def add_book(request):

    if request.method == 'POST':

        form = BookForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('/books/')

    else:

        form = BookForm()

    return render(request, 'add_book.html', {'form': form})


@login_required
def edit_book(request, id):

    book = get_object_or_404(Book, id=id)

    if request.method == 'POST':

        form = BookForm(request.POST, instance=book)

        if form.is_valid():

            form.save()

            return redirect('/books/')

    else:

        form = BookForm(instance=book)

    return render(request, 'add_book.html', {'form': form})


@login_required
def delete_book(request, id):

    book = get_object_or_404(Book, id=id)

    book.delete()

    return redirect('/books/')


@login_required
def borrow_book(request, id):

    book = get_object_or_404(Book, id=id)

    book.is_borrowed = True

    book.save()

    return redirect('/books/')


@login_required
def return_book(request, id):

    book = get_object_or_404(Book, id=id)

    book.is_borrowed = False

    book.save()

    return redirect('/books/')


def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('/login/')

    else:

        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login(request):

    if request.method == 'POST':

        form = AuthenticationForm(request, request.POST)

        if form.is_valid():

            user = form.get_user()

            auth_login(request, user)

            return redirect('/books/')

    else:

        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_user(request):

    logout(request)

    return redirect('/login/')

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Book, ActivityLog
from .forms import BookForm, RegisterForm
from datetime import date

from django.contrib.auth.forms import  AuthenticationForm
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

        form = BookForm(request.POST, request.FILES)

        if form.is_valid():

            book = form.save()

            ActivityLog.objects.create(
                user=request.user,
                action="Added Book",
                book=book,
                book_title=book.title
            )


            messages.success(request, "Book added successfully!")

            return redirect('/books/')

    else:

        form = BookForm()

    return render(request, 'add_book.html', {'form': form})


@login_required
def edit_book(request, id):

    book = get_object_or_404(Book, id=id)

    if request.method == 'POST':

        form = BookForm(request.POST, request.FILES, instance=book)

        if form.is_valid():

            updated_book = form.save()

            ActivityLog.objects.create(
                user=request.user,
                action="Updated Book",
                book=updated_book,
                book_title=updated_book.title
            )

           

            messages.success(request, "Book updated sucessfully")

            return redirect('/books/')

    else:

        form = BookForm(instance=book)

    return render(request, 'add_book.html', {'form': form})


@login_required
def delete_book(request, id):

    book = get_object_or_404(Book, id=id)

    book_title = book.title

    ActivityLog.objects.create(
        user=request.user,
        action="Deleted Book",
        book=book,
        book_title=book.title

    )

    book.delete()

    messages.success(request, "Book deleted successfully")

    return redirect('/books/')


@login_required
def borrow_book(request, id):

    book = get_object_or_404(Book, id=id)

    if not book.is_borrowed:

        book.is_borrowed = True
        book.borrow_date = date.today()
        book.return_date = None
        book.save()

        ActivityLog.objects.create(
            user=request.user,
            action="Borrowed Book",
            book=book,
            book_title=book.title
        )

    messages.success(request, "Book borrowed successfully")

    return redirect('/books/')


@login_required
def return_book(request, id):

    book = get_object_or_404(Book, id=id)

    if book.is_borrowed:

       book.is_borrowed = False
       book.return_date = date.today()
       book.save()

       ActivityLog.objects.create(
           user=request.user,
           action="Returned Book",
           book=book,
           book_title=book.title
       )

    messages.success(request, "Book returned successfully")
    return redirect('/books/')


def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('/login/')

    else:

        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login(request):

    if request.user.is_authenticated:
        return redirect('/books/')

    if request.method == 'POST':

        form = AuthenticationForm(request, request.POST)

        if form.is_valid():

            user = form.get_user()

            auth_login(request, user)

            ActivityLog.objects.create(
                user=user,
                action="Logged In"
            )

            return redirect('/books/')

    else:

        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_user(request):

    if request.user.is_authenticated:

        ActivityLog.objects.create(
            user=request.user,
            action="Logged Out"
        )

    logout(request)

    return redirect('/login/')

@login_required
def activity_log(request):

    if not request.user.is_superuser:
        return HttpResponse("Access Denied! Only the admin can view the Activity Log.")

    logs = ActivityLog.objects.all().order_by('-timestamp')

    return render(request, 'activity_log.html', {
        'logs' : logs
    })

                  

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import bcrypt
from .models import User, Book


def index(request):
    if request.session.get('uid') is None:
        return render(request, 'index.html')
    else:
        return redirect('/books')

def books(request):
    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')
    else:   
        user_from_db = User.objects.get(id=uid)
        reviews = Review.objects.all().order_by('-created_at')
        #order by negative date order
        recent_reviews = []
        count = 0
        for review in reviews:
            if count < 3:
                recent_reviews.append(review)
            count += 1

        context = {
            'user': user_from_db,
            'all_user': User.objects.all(),
            'reviews': Review.objects.all(),
            'books': Book.objects.all(),
            'recent_reviews': recent_reviews
        }
        return render(request, 'home_page.html', context)


def login(request):
    found_users = User.objects.filter(email=request.POST['email'])

    if len(found_users) < 1:
        messages.error(request, 'Invalid credentials')
        return redirect('/')
    else:
        user_from_db = found_users[0]

        is_pw_correct = bcrypt.checkpw(request.POST['password'].encode(), user_from_db.password.encode())

        if is_pw_correct is True:
            request.session['uid'] = user_from_db.id
            return redirect('/books')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def register(request):
    if User.objects.basic_validator(request) is False:
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name=request.POST['name'],
            alias=request.POST['alias'], 
            email=request.POST['email'], 
            password=hashed_pw
            )

        request.session['uid'] = new_user.id

        return redirect('/books')

def users_profile(request, id):
    uid = request.session.get('uid')

    if uid is not None:
        user_from_db = User.objects.get(id=uid)

        context = {
            'user': user_from_db
        }
        return render(request, 'users_profile.html', context)
    else:
        return redirect('/')


def add_book(request):
    uid= request.session.get('uid')

    if uid is None:
        return redirect('/')

    logged_in_user = User.objects.get(id=uid)
    authors = []
    books = Book.objects.all()

    if len(books):
        for book in books:
            authors.apppend(book.author)

    context = {
        'logged_in_user': logged_in_user,
        'books': books,
        'authors': authors
    }
    return render(request, 'add_book.html', context)

def add_validate(request):
    uid = request.session.get('uid')
    curr_user = User.objects.get(id=uid)

    if request.POST['select_author']:
        author = request.POST['select_author']
    else:
        author = request.POST['author']
        title = request.POST['title']
        new_book = Book.objects.create(title=title, author=author)
        review = request.POST['review']
        rating = request.POST['rating']
        Review.objects.create(message=review, rating=rating, created_by=curr_user, book_review=new_book)
        return redirect(f'/books/{new_book.id}')


def book_info(request, id):
    uid = request.session.get('uid')
    curr_user = User.objects.get(id=uid)
    this_book = Book.objects.get(id=id)
    reviews = Review.objects.all().order_by('-created_at')
    recent_reviews = []
    count = 0
    for review in reviews:
        if count < 3:
            recent_reviews.append(review)
        count += 1
    context = {
        'this_book': this_book,
        'this_user': curr_user,
        'reviews': reviews,
        'recent_reviews': recent_reviews
    }
    return render(request, 'book_info.html', context)


def user_info(request):
    return render(request, 'user_info.html')


def destroy(request, bid, rid):
    delete_review = Review.objects.get(id=rid)
    delete_review.delete()
    return redirect(f'/books{bid}')

from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, request):
        if len(request.POST['name']) < 1:
            messages.error(request, 'Name should be more than 1 character')

        if len(request.POST['alias']) < 1:
            messages.error(request, 'Alias should be more than 1 character')

        if not EMAIL_REGEX.match(request.POST['email']):
            messages.error(request, 'Invalid email address')

        if len(request.POST['password']) < 8:
            messages.error(request, 'Password should be at least 8 characters')

        if request.POST['password'] != request.POST['pw_check']:
            messages.error(request, 'Passwords must match')

        error_messages = messages.get_messages(request)
        error_messages.used = False
        return len(error_messages) == 0

class User(models.Model):
    first_name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Model):
    def basic_validator_book(self, request):
        errors = {}
        if len(request['title']) < 2:
            errors['title'] = 'Title of the book should be more than 2 characters'

        if len(request['author']) < 2:
            errors['author'] = 'The author field should be more than 2 characters'
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class ReviewManager(models.Model):
    def basic_validator_review(self, request):
        errors = {}
        if len(request['comment']) < 4:
            errors['comments'] = 'Please be more descriptive'

        if len(request['rating']) <= 1:
            errors['rating'] = 'Please leave a rating of one, even it completely sucks'
        return errors

class Review(models.Model):
    comment = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', related_name='reviews', on_delete=models.CASCADE)
    book_review = models.ForeignKey('Book', related_name='reviews', on_delete=models.CASCADE)
    objects = ReviewManager()






from datetime import date
from myapp.models import Book ,BookRequest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import *


User=get_user_model()

def create_book():
    book=Book.objects.create(
        title='Book 1',
        author='author 1',
        isbn='45678',   
        genre='crime',
        quantity=6

    )
    return book

  
def create_librarian_user():
    user=User.objects.create_user(
        email='student@gmail.com',
        password='test_password',
        user_type='librarian',
        username='librarianuser'

    )
    return user

def login_librarian_user(self):
    
    return self.client.login(username='librarianuser',password='test_password')

def create_student_user():
    user=User.objects.create_user(
        email='test@gmail.com',
        password='test_password',
        user_type='student',
        username='studentuser'
    )
    return user


def login_student_user(self):
    
    return self.client.login(username='studentuser',password='test_password')

def create_book_request(user,book):
    book_request=BookRequest.objects.create(
        user=user,
        book=book,
        status='pending'

    )
    return book_request

def create_approved_book_request(user,book):
    book_request=BookRequest.objects.create(
        user=user,
        book=book,
        status='approved'
    )
    return book_request

def create_token(user):
    token=Token.objects.create(
        user=user
    )
    return token


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from myapp.models import Book
from myapp.serializer import BookSerializer
from myapp.views import LibrarianRequiredMixin
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from .test_utils import *

class ListBookViewTestCase(APITestCase):
    def setUp(self):
        # Create a librarian user and generate a token
        User = get_user_model()
        self.librarian=create_librarian_user()
        self.librarian_token = Token.objects.create(user=self.librarian)
        self.student=create_student_user()
        self.student_token = Token.objects.create(user=self.student)
              
    def test_add_book_as_librarian(self):
        url = reverse('list-book')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.librarian_token.key}')
        login_librarian_user(self)

      
        new_book_data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn':"345678",
            'status':'available',
            "genre":'mystery'
        }
        

        # Make a POST request to add a new book
        response = self.client.post(url, new_book_data, format='json')

        # Check the response status code (should be 201 for created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the book was added to the database
        self.assertEqual(Book.objects.count(), 1)  # Assuming there was one book created in setUp
        self.assertEqual(Book.objects.last().title, 'New Book')

    # Add similar test cases for update and delete actions as a librarian

    def test_add_book_as_student(self):
        # Set the Authorization header with the student's token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.student_token.key}')
        login_student_user(self)

        # Create the URL for the ListBook view
        url = reverse('list-book')

        # Data for creating a new book
        new_book_data = {
            'title': 'New Book',
            'author': 'New Author',
        }

        # Make a POST request to add a new book as a student
        with self.assertRaises(PermissionDenied):
            self.client.post(url, new_book_data, format='json')
       
        self.assertEqual(Book.objects.count(), 0)






   

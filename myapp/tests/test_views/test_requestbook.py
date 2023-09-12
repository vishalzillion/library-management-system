from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from myapp.models import Book, BookRequest
from myapp.serializer import BookRequestSerializer
from myapp.views import CustomTokenAuthentication
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

class RequestBookViewTestCase(APITestCase):
    def setUp(self):
        # Create a user and generate a token
        User = get_user_model()
        self.user = User.objects.create_user(
            email='user@gmail.com',
            password='user_password',
            username='testuser',
            user_type='student'
        )
        self.token = Token.objects.create(user=self.user)

        # Create a test book
        self.book = Book.objects.create(title='Test Book', author='Test Author',isbn="67890",status='available',genre='mystery')
        self.client.login(username='testuser',password='user_password')
    def test_request_book(self):
        # Set the Authorization header with the user's token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create the URL for the RequestBook view
        url = reverse('request-book')

        # Data for requesting a book
        request_data = {
            'book_id': self.book.pk,
        }

        # Make a POST request to request a book
        response = self.client.post(url, request_data, format='json')

        # Check the response status code (should be 201 for created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that a BookRequest instance was created for the user and book
        self.assertTrue(BookRequest.objects.filter(user=self.user, book=self.book, status='pending').exists())

    def test_request_already_requested_book(self):
        # Set the Authorization header with the user's token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create a BookRequest instance for the user and book
        BookRequest.objects.create(user=self.user, book=self.book, status='pending')

        # Create the URL for the RequestBook view
        url = reverse('request-book')

        # Data for requesting a book
        request_data = {
            'book_id': self.book.pk,
        }

        # Make a POST request to request a book that is already requested
        response = self.client.post(url, request_data, format='json')

        # Check the response status code (should be 200 OK)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.data)
        # Check that the response message indicates that the book is already requested
        self.assertEqual(response.data['message'], 'This book is already requested')

    def test_request_nonexistent_book(self):
        # Set the Authorization header with the user's token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create the URL for the RequestBook view
        url = reverse('request-book')

        # Data for requesting a book with a nonexistent ID
        request_data = {
            'book_id': 999,  # Nonexistent book ID
        }

        # Make a POST request to request a nonexistent book
        response = self.client.post(url, request_data, format='json')

        # Check the response status code (should be 200 OK)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response message indicates that the book was not found
        self.assertEqual(response.data['message'], 'Book not found')

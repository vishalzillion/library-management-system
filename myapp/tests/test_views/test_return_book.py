from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from myapp.models import BookRequest
from myapp.serializer import BookRequestSerializer
from myapp.views import StudentRequiredMixin
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from myapp.models import *

class ReturnBookViewTestCase(APITestCase):
    def setUp(self):
        # Create a student user and generate a token
        User = get_user_model()
        self.student = User.objects.create_user(
            email='student@gmail.com',
            password='student_password',
            username='studentuser',
            user_type='student'
        )
        self.student_token = Token.objects.create(user=self.student)
        self.book = Book.objects.create(title='Book 1', author='Test Author',isbn="67890",status='available',genre='mystery')
        # Create a test book request
        self.book_request = BookRequest.objects.create(
            user=self.student, book=self.book, status='approved', return_status='not_returned'
        )
        self.client.login(username='studentuser',password='student_password')

    def test_return_book(self):
        # Set the Authorization header with the student's token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.student_token.key}')

        # Create the URL for the ReturnBook view
        url = reverse('return-book')

        # Data for returning the book request
        return_data = {
            'book_id': self.book_request.id
        }

        # Make a POST request to return the book
        response = self.client.post(url, return_data, format='json')

        # Check the response status code (should be 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the book request's return status is 'returned' in the database
        self.book_request.refresh_from_db()
        self.assertEqual(self.book_request.return_status, 'returned')

    def test_return_already_returned_book(self):
        # Set the Authorization header with the student's token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.student_token.key}')

        # Create the URL for the ReturnBook view
        url = reverse('return-book')

        # Set the book request's return status to 'returned'
        self.book_request.return_status = 'returned'
        self.book_request.save()

        # Data for returning the book request
        return_data = {
            'book_id': self.book_request.id
        }

        # Make a POST request to return the book (already returned)
        response = self.client.post(url, return_data, format='json')

        # Check the response status code (should be 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the book request's return status remains 'returned' in the database
        self.book_request.refresh_from_db()
        self.assertEqual(self.book_request.return_status, 'returned')

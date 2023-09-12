from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from myapp.models import BookRequest
from myapp.serializer import BookRequestActionSerializer
from myapp.views import LibrarianRequiredMixin
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from myapp.models import *
from rest_framework.exceptions import PermissionDenied


User=get_user_model()
class ListRequestedBooksViewTestCase(APITestCase):
    def setUp(self):
        # Create a librarian user and generate a token
        User = get_user_model()
        self.librarian = User.objects.create_user(
            email='librarian@gmail.com',
            password='librarian_password',
            username='librarianuser',
            user_type='librarian'
        )
        self.librarian_token = Token.objects.create(user=self.librarian)
        self.book1 = Book.objects.create(title='Book 1', author='Test Author',isbn="67890",status='available',genre='mystery')
        self.book2 = Book.objects.create(title='Book 2', author='Test Author 2',isbn="67890",status='available',genre='mystery')
        self.client.login(username='testuser',password='user_password')
        # Create some test book requests
        self.book_request1 = BookRequest.objects.create(
            user=self.librarian, book=self.book1, status='approved'
        )
        self.book_request2 = BookRequest.objects.create(
            user=self.librarian, book=self.book2, status='pending'
        )
        
    def test_list_requested_books_as_librarian(self):
        # Set the Authorization header with the librarian's token
       
        self.client.login(username='librarianuser',password='librarian_password')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.librarian_token.key}')


        # Create the URL for the ListRequestedBooks view
        url = reverse('list-requested-books')

        # Make a GET request to list requested books
        response = self.client.get(url)

        # Check the response status code (should be 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data contains the expected book requests
        expected_data = BookRequestActionSerializer([self.book_request1, self.book_request2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_list_requested_books_as_student(self):
        # Create a student user and generate a token
        self.student = User.objects.create_user(
            email='student@gmail.com',
            password='student_password',
            username='studentuser',
            user_type='student'
        )
        student_token = Token.objects.create(user=self.student)
        self.client.login(username='studentnuser',password='student_password')

        # Set the Authorization header with the student's token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {student_token.key}')

        # Create the URL for the ListRequestedBooks view
        url = reverse('list-requested-books')

        with self.assertRaises(PermissionDenied):
            self.client.post(url,format='json')

        # Check the response status code (should be 403 Forbidden)
 

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from myapp.models import Book  # Import your Book model
from myapp.serializer import BookSerializer  # Import your BookSerializer
from myapp.views import CustomPagination
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .test_utils import *

class AllBooksViewTestCase(APITestCase):
    def setUp(self):
        # Create a test user and generate a token
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
        )
        self.token = Token.objects.create(user=self.user)

        # Create some test books
        self.book1 = Book.objects.create(title='Book 1', author='Author 1')
        self.book2 = Book.objects.create(title='Book 2', author='Author 2')
        self.book3 = Book.objects.create(title='Book 3', author='Author 3')
        self.book4 = Book.objects.create(title='Book 4', author='Author 5')
        self.book6 = Book.objects.create(title='Book 6', author='Author 6')
        self.book5 = Book.objects.create(title='Book 5', author='Author 5')

    def test_list_all_books(self):
    # Set the Authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create the URL for the AllBooks view
        url = reverse("all-book")  # Replace "all-books" with the actual URL name

        # Make a GET request to list all books
        response = self.client.get(url)

        # Check the response status code (should be 200 for successful retrieval)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the 'results' key in the response data matches the serialized books
        expected_data = BookSerializer([self.book1, self.book2,self.book3,self.book4,self.book6], many=True).data
        self.assertEqual(response.data['results'], expected_data)


    def test_list_books_with_search(self):
        # Set the Authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create the URL for the AllBooks view with a search query
        url = reverse("all-book") + "?search=Book 1"  # Replace "all-books" with the actual URL name

        # Make a GET request to list books with a search query
        response = self.client.get(url)

        # Check the response status code (should be 200 for successful retrieval)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains only the book(s) matching the search query
        expected_data = BookSerializer([self.book1], many=True).data
        self.assertEqual(response.data['results'], expected_data)

    
    
    
    def test_book_using_custom_pagination(self):
    # Set the Authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create the URL for the AllBooks view with a page query parameter
        url = reverse("all-book") + "?page=2"  # Replace "all-book" with the actual URL name

        # Make a GET request to fetch paginated data (page 2)
        response = self.client.get(url)

        # Check the response status code (should be 200 for successful retrieval)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the 'results' key in the response data contains the expected serialized books
        expected_data = BookSerializer([self.book5], many=True).data
        self.assertEqual(response.data['results'], expected_data)
        print(create_book())

     
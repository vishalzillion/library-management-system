from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from myapp.models import Book
from myapp.serializer import BookSerializer
from myapp.views import LibrarianRequiredMixin
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

class ListBookViewTestCase(APITestCase):
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

        # Create a test book
        self.book = Book.objects.create(title='Test Book', author='Test Author',isbn='5879',status='available', genre='crime')
        self.client.login(username='librarianuser',password='librarian_password')

    def test_create_book_as_librarian(self):
        # Set the Authorization header with the librarian's token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.librarian_token.key}')

        # Create the URL for the ListBook view
        url = reverse('list-book')

        # Data for creating a new book
        new_book_data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn':"56789",
            "status":"available",
            "genre":"drama"
        }

        # Make a POST request to add a new book
        response = self.client.post(url, new_book_data, format='json')

        # Check the response status code (should be 201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the book was added to the database
        self.assertEqual(Book.objects.count(), 2)  # Assuming there was one book created in setUp
        self.assertEqual(Book.objects.last().title, 'New Book')

    def test_update_book_as_librarian(self):
        # Set the Authorization header with the librarian's token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.librarian_token.key}')

        # Create the URL for the ListBook view with the book's ID
        url = reverse('list-book-detail', args=[self.book.id])
        print(self.book)
        # Data for updating the book
        updated_book_data = {
            'title': 'Updated Book Title',
            'author': 'Updated Author',
            'isbn':"567899990",
            "status":'available',
            "genre":"drama"
        }


        # Make a PUT request to update the book
        response = self.client.put(url, updated_book_data, format='json')
        self.book.refresh_from_db()
        print(self.book)

        # Check the response status code (should be 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the book's details were updated in the database
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book Title')
    #     self.assertEqual(self.book.author, 'Updated Author')

    def test_delete_book_as_librarian(self):
        # Set the Authorization header with the librarian's token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.librarian_token.key}')

        # Create the URL for the ListBook view with the book's ID
        url = reverse('list-book-detail', args=[self.book.id])

        # Make a DELETE request to delete the book
        response = self.client.delete(url)

        # Check the response status code (should be 204 No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check that the book was deleted from the database
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

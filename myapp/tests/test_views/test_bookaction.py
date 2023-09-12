from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from myapp.models import Book, BookRequest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

class BookRequestActionViewTestCase(TestCase):
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

        # Create a test book with some quantity
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            quantity=5,
        )

        # Create a test book request
        self.book_request = BookRequest.objects.create(
            user=self.librarian,
            book=self.book,
            status=BookRequest.PENDING,
            return_status=BookRequest.NOT_RETURNED,
        )

        # Create an API client and set the Authorization header
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.librarian_token.key}')
        self.client.login(username='librarianuser',password='librarian_password')

    def test_approve_request(self):
        book_request_id=self.book_request.id
        data={
            "book_request_id":book_request_id
        }
        # Create the URL for approving the book request
        url = reverse('approve-book-request')

        # Make a POST request to approve the book request
        response = self.client.post(url,data=data)
        print(response.data)
        # Check the response status code (should be 200 for success)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       

        # Check that the book request's status is now APPROVED
        self.book_request.refresh_from_db()
        self.assertEqual(self.book_request.status, BookRequest.APPROVED)

        # Check that the book's quantity is decreased by 1
        self.book.refresh_from_db()
        self.assertEqual(self.book.quantity, 4)


    def test_reject_request(self):
        book_request_id=self.book_request.id
        data={
            "book_request_id":book_request_id
        }
        # Create the URL for rejecting the book request
        url = reverse('reject-book-request')

        # Make a POST request to reject the book request
        response = self.client.post(url,data=data)
        

        # Check the response status code (should be 200 for success)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the book request's status is now REJECTED
        self.book_request.refresh_from_db()
        self.assertEqual(self.book_request.status, BookRequest.REJECTED)

    def test_revoke_request(self):
        # Set the book request's status to APPROVED
        self.book_request.status = BookRequest.APPROVED
        self.book_request.save()

        self.book_request.refresh_from_db()

        book_request_id=self.book_request.id

        data={
            "book_request_id":book_request_id
        }

        # Create the URL for revoking the book request
        url = reverse('revoke-book-request')

        # Make a POST request to revoke the book request
        response = self.client.post(url,data=data)

        # Check the response status code (should be 200 for success)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the book request's status is now COMPLETED
        self.book_request.refresh_from_db()
        self.assertEqual(self.book_request.status, BookRequest.COMPLETED)

        # Check that the book's quantity is increased by 1
        self.book.refresh_from_db()
        self.assertEqual(self.book.quantity, 6)

 

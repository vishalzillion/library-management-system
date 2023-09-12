from unittest.mock import Mock
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, Mock
from django.core import mail
from myapp.models import Book, BookRequest
from myapp.serializer import BookRequestSerializer
from .test_utils import *
from rest_framework.settings import *
from rest_framework.authtoken.models import Token

class RequestBookTestCase(APITestCase):

    def setUp(self):
        self.user=create_librarian_user()
        self.book=create_book()
        login_librarian_user(self)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        


    @patch('myapp.views.send_mail') 
    def test_request_book(self, mock_send_mail):
        
        serializer_data = {'book_id': self.book.id}
        serializer = BookRequestSerializer(data=serializer_data, context={'request': self.user})

        # Mock the BookRequest.objects.filter method to return an empty list (no previous requests)
        with patch.object(BookRequest.objects, 'filter', return_value=[]):
            response = self.client.post('/request-book/', serializer_data, format='json')
        
        
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'message': 'Book request submitted successfully'})

        # Check that send_mail was called with the expected arguments
        mock_send_mail.assert_called_once_with(
            subject='Book Request Has been Submitted',
            message=f'Your book request for "{self.book.title}"',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
        )

    @patch('myapp.views.send_mail')  # Mock the send_mail function
    def test_duplicate_book_request(self, mock_send_mail):
        
        book = Book.objects.create(title='Sample Book', author='John Doe', isbn='1234567890')

        # Create a mock serializer instance with valid data
        serializer_data = {'book_id': self.book.id}
        serializer = BookRequestSerializer(data=serializer_data, context={'request': self.user})

        # Mock the BookRequest.objects.filter method to return a previous request
        with patch.object(BookRequest.objects, 'filter', return_value=[Mock()]):
            response = self.client.post('/request-book/', serializer_data, format='json')
        print(response)
        # Check that the response is as expected
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'message': 'This book is already requested'})

        # Ensure that send_mail was not called in this case
        mock_send_mail.assert_not_called()

# Here we are mocking the filter method to return_value according to our need


    def test_json_response(self):
        # Create a mock function
        mocked_function = Mock()

       
        json_response = {
            "key1": "value1",
            "key2": "value2",
        }

        mocked_function.return_value = json_response

        # Call the mocked function
        result = mocked_function()

        # Check the result (it will be the JSON response)
        print(result)


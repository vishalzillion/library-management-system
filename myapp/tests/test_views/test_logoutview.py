from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from myapp.models import User  # Import your User model
from myapp.serializer import UserSerializer  # Import your UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

class UserLogoutViewTestCase(APITestCase):
    def setUp(self):
        # Create a test user and generate a token
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
        )
        self.token = Token.objects.create(user=self.user)

    def test_user_logout(self):
        # Set the Authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create the URL for the logout view
        url = reverse("user-logout")  # Replace "user-logout" with the actual URL name

        # Make a POST request to the logout view
        response = self.client.post(url)

        # Check the response status code (should be 200 for successful logout)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the token associated with the user has been deleted
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_unauthenticated_user_logout(self):
        # Create the URL for the logout view
        url = reverse("user-logout")  # Replace "user-logout" with the actual URL name

        # Make a POST request to the logout view without setting the token
        response = self.client.post(url)

        # Check the response status code (should be 401 for unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Check that the response contains a message indicating the user is not authenticated
        # self.assertIn("message", response.data)
       
        self.assertEqual(response.data["detail"], "Token is required to authenticate")


    def tearDown(self):
        # Clean up after the tests (e.g., delete the test user and token)
        self.token.delete()
        self.user.delete()

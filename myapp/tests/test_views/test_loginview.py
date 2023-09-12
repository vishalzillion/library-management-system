from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from myapp.models import User  # Import your User model
from myapp.serializer import UserSerializer 
from django.contrib.auth import get_user_model 
from myapp.serializer import * 
from rest_framework.exceptions import ValidationError  # Import your UserSerializer

User=get_user_model()




class UserLoginViewTestCase(APITestCase):
    def setUp(self):
        # Create a test user for login
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
            is_active=True
        )

    def test_user_login(self):
        # Define user login data
        login_data = {
            "username": "testuser",
            "password": "testpassword",
        }

        # Create the URL for the login view
        url = reverse("user-login")  # Replace "user-login" with the actual URL name

        # Make a POST request to the login view with login data
        response = self.client.post(url, login_data, format="json")

        # Check the response status code (should be 200 for successful login)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains a token
        self.assertIn("token", response.data)
        self.assertTrue(response.data["token"].startswith("Token"))

   

    def test_invalid_user_login(self):
        # Define invalid user login data (incorrect password)
        invalid_login_data = {
            "username": "testuser",
            "password": "invalidpassword",
        }

        # Create the URL for the login view
        url = reverse("user-login")  # Replace "user-login" with the actual URL name

        # Make a POST request to the login view with invalid login data
        response = self.client.post(url, invalid_login_data, format="json")

        # Check the response status code (should be 401 for unauthorized)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
# 
        # Check that the response contains a message about invalid credentials
        # self.assertIn("message", response.data)
        self.assertEqual(response.data["non_field_errors"][0], "Unable to log in with provided credentials.")

   





# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from myapp.models import User  # Import your User model
# from myapp.serializer import UserSerializer 
# from django.contrib.auth import get_user_model # Import your UserSerializer


# User=get_user_model()
# class UserSignupViewTestCase(APITestCase):
#     def setUp(self):
#         # Create a user with an existing email address in the database
#         existing_user = User.objects.create_user(
#             username='existinguser',
#             password='existingpassword',
#             user_type=User.STUDENT,
#             phone_number='9876543210',
#             first_name='Jane',
#             last_name='Smith',
#             age=30,
#             email='existinguser@example.com'
#         )
#     def test_user_signup(self):
#         # Define the user data for registration
#         user_data = {
#             "username": "testuser",
#             "password": "testpassword",
#             "user_type": "student",
#             "phone_number": "1234567890",
#             "first_name": "John",
#             "last_name": "Doe",
#             "age": 25,
#             "email": "testuser@example.com",
#         }

#         # Create the URL for the signup view
#         url = reverse("user-signup")  # Replace "user-signup" with the actual URL name

#         # Make a POST request to the signup view with user data
#         response = self.client.post(url, user_data, format="json")

#         # Check the response status code (should be 201 for successful creation)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # Check if a user was created in the database
#         self.assertTrue(User.objects.filter(username="testuser").exists())

#         # Check if a token was generated and returned in the response
#         self.assertIn("token", response.data)
#         self.assertTrue(response.data["token"].startswith("Token "))

#         # Optionally, you can also check the response data for user details
#         self.assertIn("detail", response.data)
#         self.assertEqual(response.data["detail"], UserSerializer(User.objects.get(username="testuser")).data)

#     def test_invalid_user_signup(self):
#         # Define invalid user data (missing required fields)
#         invalid_user_data = {
#             "username": "testuser2",
#             "password": "testpassword2",
#         }

#         # Create the URL for the signup view
#         url = reverse("user-signup")  # Replace "user-signup" with the actual URL name

#         # Make a POST request to the signup view with invalid user data
#         response = self.client.post(url, invalid_user_data, format="json")

#         # Check the response status code (should be 400 for bad request)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#         # Check that the response contains error messages
#         # self.assertIn("user_type", response.data)
#         self.assertIn("phone_number", response.data)

#         self.assertIn("email", response.data)



#     # def test_invalid_user_signup(self):
#     #     # Define user data with an existing email address
#     #     invalid_user_data = {
#     #         "username": "testuser2",
#     #         "password": "testpassword2",
#     #         "user_type": "student",
#     #         "phone_number": "1234567890",
#     #         "first_name": "John",
#     #         "last_name": "Doe",
#     #         "age": 25,
#     #         "email": "existinguser@example.com",  # Use an existing email address here
#     #     }

#     #     # Create the URL for the signup view
#     #     url = reverse("user-signup")  # Replace "user-signup" with the actual URL name

#     #     # Make a POST request to the signup view with invalid user data
#     #     response = self.client.post(url, invalid_user_data, format="json")

#     #     # Check the response status code (should be 400 for bad request)
#     #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     #     # Check that the response contains an error message about the existing email address
#     #     self.assertIn("email", response.data)
#     #     self.assertEqual(response.data["email"][0], "user with this email already exists.")




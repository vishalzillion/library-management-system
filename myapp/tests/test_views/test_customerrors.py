from django.test import TestCase
from myapp.views import custom_exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

class CustomExceptionHandlerTestCase(TestCase):
    def test_custom_exception_handler(self):
        # Create a sample ValidationError with field errors
        validation_error = ValidationError({
            'field1': ['Error message 1'],
            'field2': ['Error message 2', 'Error message 3'],
        })

        # Call the custom_exception_handler with the validation_error
        response = custom_exception_handler(validation_error)

        # Check that the response is a Response instance
        self.assertIsInstance(response, Response)

        # Check the status code (should be 400 for bad request)
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the response content
        expected_response = {
            "errors": {
                "display_error": "Invalid Input",
                "field_errors": {
                    "field1": ["Error message 1"],
                    "field2": ["Error message 2", "Error message 3"]
                }
            }
        }
        self.assertEqual(response.data, expected_response)

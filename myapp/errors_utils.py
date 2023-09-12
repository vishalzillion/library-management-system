from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import serializers



def custom_exception_handler(exc):
    if isinstance(exc, serializers.ValidationError):
        errors = {}
        field_errors = {}

        for field, messages in exc.detail.items():
            if isinstance(messages, list):
                field_errors[field] = messages
            else:
                errors[field] = messages

        custom_response = {
            "errors": {
                "display_error": "Invalid Input",
                "field_errors": field_errors,
            }
        }
        return Response(custom_response)

    return None  # Return None if the exception is not handled





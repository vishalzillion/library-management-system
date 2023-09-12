from django.test import TestCase


from django.test import TestCase
from myapp.models import User  # Import your User model from the appropriate module
from django.db import IntegrityError

class UserModelTestCase(TestCase):
    def setUp(self):
        # Create a test user for your model
        self.user = User.objects.create(
            username='testuser',
            password='testpassword',
            user_type=User.STUDENT,
            phone_number='1234567890',
            first_name='John',
            last_name='Doe',
            age=25,
            email='testuser@example.com'
        )

    def test_user_creation(self):
        # Test that the user was created correctly
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.user_type, User.STUDENT)
        self.assertEqual(self.user.phone_number, '1234567890')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.age, 25)
        self.assertEqual(self.user.email, 'testuser@example.com')

    def test_user_string_representation(self):
        # Test the __str__ method of the User model
        expected_str = 'testuser'
        self.assertEqual(str(self.user), expected_str)

    def test_unique_email_constraint(self):
        # Test that email field has a unique constraint
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username='anotheruser',
                password='anotherpassword',
                user_type=User.LIBRARIAN,
                phone_number='9876543210',
                first_name='Jane',
                last_name='Smith',
                age=30,
                email='testuser@example.com'  # Attempt to create a user with the same email
            )
            
from django.test import TestCase
from myapp.models import BookRequest, Book
from django.contrib.auth import get_user_model
from django.utils import timezone

class BookRequestModelTestCase(TestCase):
    def setUp(self):
        # Create a sample user
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )

        # Create a sample book
        self.book = Book.objects.create(
            title='Sample Book',
            author='Sample Author',
            quantity=5,
        )

        # Create a sample book request
        self.request = BookRequest.objects.create(
            user=self.user,
            book=self.book,
            status=BookRequest.PENDING,
            return_status=BookRequest.NOT_RETURNED,
        )

    def test_approve_request(self):
        # Check that status is initially PENDING
        self.assertEqual(self.request.status, BookRequest.PENDING)

        # Call the approve_request method
        self.request.approve_request()

        # Check that status is now APPROVED
        self.assertEqual(self.request.status, BookRequest.APPROVED)

        # Check that approval_date is set
        self.assertIsNotNone(self.request.approval_date)

        # Check that book quantity is decreased by 1
        self.assertEqual(self.book.quantity, 4)

    def test_reject_request(self):
        # Check that status is initially PENDING
        self.assertEqual(self.request.status, BookRequest.PENDING)

        # Call the reject_request method
        self.request.reject_request()

        # Check that status is now REJECTED
        self.assertEqual(self.request.status, BookRequest.REJECTED)

    def test_revoke_request(self):
        # Set the request status to APPROVED
        self.request.status = BookRequest.APPROVED
        self.request.save()
      

        # Check that status is initially APPROVED
        self.assertEqual(self.request.status, BookRequest.APPROVED)

        # Call the revoke_request method
        self.request.revoke_request()
        self.request.refresh_from_db()

        # Check that status is now COMPLETED
        self.assertEqual(self.request.status, BookRequest.COMPLETED)

        # Check that return_status is REVOKED
        self.assertEqual(self.request.return_status, BookRequest.REVOKED)

        # Check that book quantity is increased by 1
        self.assertEqual(self.book.quantity, 6)

    def test_return_request(self):
        # Set the request status to APPROVED and return_status to NOT_RETURNED
        self.request.status = BookRequest.APPROVED
        self.request.return_status = BookRequest.NOT_RETURNED
        self.request.save()

        # Check that status is initially APPROVED
        self.assertEqual(self.request.status, BookRequest.APPROVED)

        # Call the return_request method
        self.request.return_request()
        self.request.refresh_from_db()

        # Check that status is now COMPLETED
        self.assertEqual(self.request.status, BookRequest.COMPLETED)

        # Check that return_status is RETURNED
        self.assertEqual(self.request.return_status, BookRequest.RETURNED)

        # Check that return_date is set
        self.assertIsNotNone(self.request.return_date)

        # Check that book quantity is increased by 1
        self.assertEqual(self.book.quantity, 6)

 
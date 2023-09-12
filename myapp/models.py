from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    STUDENT ='student'
    LIBRARIAN = 'librarian'
    USER_TYPE_CHOICES = (
        (STUDENT, 'Student'),
        (LIBRARIAN, 'Librarian'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='Student')
    phone_number = models.CharField(max_length=15)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.PositiveIntegerField(null=True, blank=True)
    email=models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Book(models.Model):
    AVAIALBLE = 'available'
    NOT_AVAILABLE = 'not_available'
    STATUS_CHOICES = (
        (AVAIALBLE, 'Available'),
        (NOT_AVAILABLE, 'Not Available'),
    )

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    # publication_date = models.DateField()
    isbn = models.CharField(max_length=13)
    genre = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    # assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    cover_image = models.FileField(upload_to='book_covers/',default='demo.jpg')
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title



class BookRequest(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    COMPLETED = 'completed'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (COMPLETED, 'Completed'),
    )

    NOT_RETURNED ='not_returned'
    RETURNED = 'returned'
    REVOKED = 'revoked'
    RETURN_STATUS_CHOICES = (
        (NOT_RETURNED, 'Not Returned'),
        (RETURNED, 'Returned'),
        (REVOKED, 'Revoked')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    approval_date = models.DateTimeField(null=True, blank=True)
    renewal_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    return_status = models.CharField(max_length=20, choices=RETURN_STATUS_CHOICES,default='not_returned')
      
    def approve_request(self):

        if self.status == self.PENDING:
            self.status = self.APPROVED
            self.approval_date = timezone.now()
            self.save()
            

            # Decrease the quantity of the associated book by 1
            if self.book:
                self.book.quantity -= 1
                self.book.save()

    def reject_request(self):
        if self.status == self.PENDING:
            self.status = self.REJECTED
            self.save()

    def revoke_request(self):
        if self.status == self.APPROVED:
            # Increase the quantity of the associated book by 1
            if self.book:
                self.book.quantity += 1
                self.book.save()

            # Set return_status to Revoked
            self.return_status = self.REVOKED
            self.status = self.COMPLETED
            self.save()     

    def return_request(self):
        if self.return_status == self.NOT_RETURNED:
            self.status = self.COMPLETED
            self.return_status = self.RETURNED
            self.return_date = timezone.now()
            if self.book:
                self.book.quantity += 1
                self.book.save()
            
            self.save()

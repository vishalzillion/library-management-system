

# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.contrib.auth import login, logout,authenticate
from rest_framework.authentication import TokenAuthentication
from .custommixins import *
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from django.db.models import Q
from rest_framework.generics import ListAPIView
from .custom import *
from .custommixins import *
from .errors_utils import *
from .authentication import CustomTokenAuthentication
from rest_framework.decorators import authentication_classes
from django.core.mail import send_mail
from rest_framework.settings import *


# sign up view
class UserSignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token, created = Token.objects.get_or_create(user=user)
                login(request,user)
                return Response({'token': "Token " + token.key,'detail':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# logout view

class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]
  


    def post(self, request):
        user = request.user
        if user.is_authenticated:
            # Delete the user's token
            Token.objects.get(user=user).delete()
            logout(request)
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

# login view
@authentication_classes([])
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )

            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': "Token" + token.key})
            
            return Response({'message': 'Unable to log in with provided credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class AllBooks(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        search_query = self.request.query_params.get('search')

        queryset = super().get_queryset()
        
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(author__icontains=search_query))

        return queryset.order_by('id')

# If needed, you can still keep your other view classes


  

# list all books to every user,where student can only get the books while librarian can edit,delete and update books

class ListBook(LibrarianRequiredMixin,APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

      
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'message':'Book added successfully',"user":request.user.user_type}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     
   
      

    def put(self, request, pk):
        user = request.user

        if user.user_type == 'librarian':
            try:
                book = Book.objects.get(pk=pk)
            except Book.DoesNotExist:
                return Response({'message': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data={'message': 'Book updated successfully'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Only librarians can update books'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        user = request.user

        
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({'message': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        book.delete()
        return Response(data={'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    


#  student can request books



from rest_framework.generics import CreateAPIView


class RequestBook(CreateAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookRequestSerializer

    def perform_create(self, serializer):
       
        user = self.request.user
        book_id = serializer.validated_data['book_id']
        response_msg = None  
        try:
            book = Book.objects.get(pk=book_id)
            book_request = BookRequest.objects.filter(user=user, book=book, status__in=['pending', 'approved'])
            if len(book_request) == 0:
            # Create a BookRequest instance
                serializer.save(user=user, book=book, status='pending')
                send_mail(
                    subject='Book Request Has been Submitted',
                    message=f'Your book request for "{book.title}"',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
              
                response_msg = {'message': 'Book request submitted successfully'}
            else:
                response_msg = {'message': 'This book is already requested'}

        except Book.DoesNotExist:
            response_msg = {'message': 'Book not found'}
            serializer._validated_data['response_msg'] = response_msg  # Store response_msg in validated_data
            
       
       

        serializer._validated_data['response_msg'] = response_msg 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response_msg = serializer.validated_data.get('response_msg', None)  # Get response_msg from validated_data
            if response_msg:
                return Response(response_msg, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return custom_exception_handler(e)

                    

    


        
      
        
# librarian can approve , reject, and revoke student book request

class BookRequestAction(LibrarianRequiredMixin,APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

    
        serializer = BookActionSerializer(data=request.data)
        if serializer.is_valid():
            book_request_id = serializer.validated_data['book_request_id']
            action = request.path.split('/')[-2]  # Extract the action from the URL path

            try:
                book_request = BookRequest.objects.get(pk=book_request_id)
            except BookRequest.DoesNotExist:
                return Response({'message': 'Book request not found'}, status=status.HTTP_404_NOT_FOUND)

            if book_request.book.quantity == 0:
                book_request.book.status == Book.NOT_AVAILABLE
                return Response({'message': "book is currently unavailable"})    

            else:  

                if action == 'approve':
                    # Approve the book request
                    book_request.approve_request()
                elif action == 'reject':
                    # Reject the book request
                    book_request.reject_request()
                elif action == 'revoke':
                    # Revoke the book request
                    book_request.revoke_request()

            return Response({'message': f'Book request {action}ed successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
     

# this will return all the requested books 

class ListRequestedBooks(LibrarianRequiredMixin,APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

      
            # Get all requested books (status is pending or approved)
        requested_books = BookRequest.objects.all()
        serializer = BookRequestActionSerializer(requested_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # If the user is not a librarian, deny access
        

class ReturnBook(StudentRequiredMixin,APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        user=request.user
        
        serializer=BookRequestSerializer(data=request.data)
        if serializer.is_valid():
            book_id=serializer.validated_data['book_id']
            try:
                book_request = BookRequest.objects.get(pk=book_id)
        
            except:
                return Response({'message': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

            if book_request.user == user :
                if book_request.return_status == "returned":
                    return Response({'message': 'Book is already returned'}, status=status.HTTP_200_OK)
                else:
                    
                    book_request.return_request()
                    return Response({'message': 'Book request return successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"you can't return this book "})         

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

             



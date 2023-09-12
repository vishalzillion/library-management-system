
from django.contrib import admin
from django.urls import path
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('listbook/', ListBook.as_view(), name='list-book'),
    path('listbook/<int:pk>/', ListBook.as_view(), name='list-book-detail'),
    path('request-book/', RequestBook.as_view(), name='request-book'),
    path('return-book/', ReturnBook.as_view(), name='return-book'),
    path('bookrequest/approve/', BookRequestAction.as_view(), name='approve-book-request'),
    path('bookrequests/', ListRequestedBooks.as_view(), name='list-requested-books'),
    path('bookrequest/reject/', BookRequestAction.as_view(), name='reject-book-request'),
    path('bookrequest/revoke/', BookRequestAction.as_view(), name='revoke-book-request'),
    path('allbooks/', AllBooks.as_view(), name='all-book'),
  

]

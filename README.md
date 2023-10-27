# library-management-system
this rest-api created using django-rest-framework
Library Management REST API
This is a REST API for a library management system built using Django REST Framework.

Features
User authentication system with JSON Web Tokens
CRUD APIs for books
Custom pagination
Search books by title and author
Different permission levels for students and librarians
Endpoints
/api/signup/ - Sign up new user
/api/login/ - Login user and retrieve JWT token
/api/logout/ - Logout user
/api/books/ - Retrieve paginated list of books, search using ?search=
/api/books/ - Create a new book (librarians only)
/api/books/<id>/ - Retrieve, update or delete a book (librarians only)
Technologies Used
Django
Django REST Framework
JWT Authentication
Setup
Install dependencies: pip install -r requirements.txt
Run migrations: python manage.py migrate
Run development server: python manage.py runserver
Usage
The API can be accessed from http://localhost:8000/api/.

Retrieve a JWT token by providing username and password to /api/login/ endpoint. Provide the token in the Authorization header as "Bearer <token>" to access protected resources.

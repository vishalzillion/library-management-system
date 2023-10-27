

# Library Management REST API

This is a REST API for a library management system built using Django REST Framework.

## Features

- User authentication system with JSON Web Tokens
- CRUD APIs for books
- Custom pagination
- Search books by title and author
- Different permission levels for students and librarians

## Endpoints

- `signup/` - Sign up new user 
- `login/` - Login user and retrieve JWT token
- `logout/` - Logout user
- `books/` - Retrieve paginated list of books, search using `?search=`
- `listbook/` - Create a new book (librarians only)
- `book/<id>/` - Retrieve, update or delete a book (librarians only)

- `request-book/` - Request a book 
- `return-book/` - Return a booked book
- `bookrequests/` - List requested books (librarians only) 
- `bookrequest/approve/` - Approve book request (librarians only)
- `bookrequest/reject/` - Reject book request (librarians only)  
- `bookrequest/revoke/` - Revoke approval for booked book (librarians only)

## Usage

### Installation

- Clone the repository 
- Create and activate a virtual environment
- Install dependencies: `pip install -r requirements.txt`

### Setup

- Run migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`

### Run Server

- Start development server: `python manage.py runserver`

The API will be available at `http://127.0.0.1:8000/`

### Testing

- Run tests: `python manage.py test`

This will run the test cases for the API.

Retrieve a JWT token by providing username and password to `login/` endpoint. Provide the token in the Authorization header as "Bearer <token>" to access protected resources.



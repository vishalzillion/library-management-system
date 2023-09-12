
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT=1
DEFAULT_SIZE=5

class CustomPagination(PageNumberPagination):
    page = DEFAULT
    page_number = page
    page_size = DEFAULT_SIZE
    print(type(page_number))

    def get_paginated_response(self, data):
        total_results = len(data)
        print(type(self.page_number))
        print(type(self.page_size))
        start = (self.page_number - 1) * self.page_size
        end = start + self.page_size

        paginated_data = data[start:end]

        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.page.paginator.count,
            'page': self.page_number,
            'limit': self.page_size,
            'total_results': total_results,
            'results': paginated_data
        })


#  <class 'django.core.paginator.Page'>
# <class 'int'>
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "content": data,
            "page": {
                "size": self.page.paginator.per_page,
                "total_pages": self.page.paginator.num_pages,
                "total_elements": self.page.paginator.count,
                "number": self.page.number
            }
        })
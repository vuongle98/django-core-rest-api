from rest_framework.pagination import PageNumberPagination


class MenuPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'  # Allows the client to set the page size
    max_page_size = 50  # Maximum number of items per page to prevent overload
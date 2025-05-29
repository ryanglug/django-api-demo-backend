from rest_framework.pagination import PageNumberPagination


class CustomPageSizePagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = "page_size"  # Allows optional page_size argument
    max_page_size = 100  # Limits maximum size to prevent performance issues

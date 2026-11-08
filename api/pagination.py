from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_query_param = "pagina"
    page_size_query_param = "tamano"
    page_size = 50
    max_page_size = 200

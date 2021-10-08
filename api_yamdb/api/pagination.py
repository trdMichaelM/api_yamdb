from rest_framework.pagination import PageNumberPagination

class ReviewsPagination(PageNumberPagination):
    page_size = 2 

class CommentsPagination(PageNumberPagination):
    page_size = 3 

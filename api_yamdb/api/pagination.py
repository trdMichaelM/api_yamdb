from rest_framework.pagination import PageNumberPagination


class UserPagination(PageNumberPagination):
    page_size = 5

class ReviewsPagination(PageNumberPagination):
    page_size = 2 

class CommentsPagination(PageNumberPagination):
    page_size = 4

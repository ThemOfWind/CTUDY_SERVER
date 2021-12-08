from rest_framework.response import Response
from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    """
    Django 페이지네이션 커스터마이징 클래스
    """
    def get_paginated_response(self, data):
        """
        return data 커스터마이징
        """
        return_data = data
        return_data['response']['page'] = self.page.number
        return_data['response']['next'] = self.get_next_link()
        return_data['response']['previous'] = self.get_previous_link()
        return_data['response']['totalCount'] = self.page.paginator.count
        return_data['response']['firstPage'] = 1
        return_data['response']['endPage'] = self.page.paginator.num_pages

        return Response(return_data)

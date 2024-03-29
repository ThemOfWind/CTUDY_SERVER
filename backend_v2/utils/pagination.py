import re
from collections import OrderedDict
from typing import Any, Optional, Type, Union

from django.core.paginator import InvalidPage, Page, Paginator
from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Schema
from ninja.pagination import PaginationBase
from ninja.types import DictStrAny
from pydantic import Field

from ninja_extra.conf import settings
from ninja_extra.schemas import PaginatedResponseSchema
from ninja_extra.urls import remove_query_param, replace_query_param

from rest_framework.response import Response
from rest_framework import pagination

from utils.error import CtudyException, not_found_error_return


def _positive_int(
    integer_string: Union[str, int], strict: bool = False, cutoff: Optional[int] = None
) -> int:
    """
    Cast a string to a strictly positive integer.
    """
    ret = int(integer_string)
    if ret < 0 or (ret == 0 and strict):
        raise ValueError()
    if cutoff:
        return min(ret, cutoff)
    return ret


class PageNumberPaginationExtra(PaginationBase):
    class Input(Schema):
        page: int = Field(1, gt=0)
        max_page: int = Field(100, lt=200)

    class Output(Schema):
        count: int
        next: str = None

    page_query_param = "page"
    page_size_query_param = "max_page"

    max_page_size = 200
    paginator_class = Paginator

    def __init__(
        self,
        max_page: int = settings.PAGINATION_PER_PAGE,
        max_page_size: Optional[int] = None,
        pass_parameter: Optional[str] = None,
    ) -> None:
        super().__init__(pass_parameter=pass_parameter)
        self.max_page = max_page
        self.max_page_size = max_page_size or 200
        self.Input = self.create_input()  # type:ignore

    def create_input(self) -> Type[Input]:
        class DynamicInput(PageNumberPaginationExtra.Input):
            page: int = Field(1, gt=0)
            max_page: int = Field(self.max_page, lt=self.max_page_size)

        return DynamicInput

    def paginate_queryset(  # type: ignore
        self,
        queryset: QuerySet,
        pagination: Input,
        request: Optional[HttpRequest] = None,
        **params: DictStrAny,
    ) -> Any:
        if isinstance(queryset, tuple) and re.match(r'20\d', str(queryset[0])):
            queryset = queryset[1]

        max_page = self.get_page_size(pagination.max_page)
        current_page_number = pagination.page
        paginator = self.paginator_class(queryset, max_page)
        try:
            page: Page = paginator.page(current_page_number)
            return self.get_paginated_response(page=page)
        except InvalidPage:
            raise CtudyException(code=404, message=not_found_error_return)

    def get_paginated_response(self, *, page: Page) -> DictStrAny:
        return OrderedDict(
            [
                ("count", page.paginator.count),
                ("next", self.get_next_link(page=page)),
                ("items", list(page)),
            ]
        )

    @classmethod
    def get_response_schema(
        cls, response_schema: Union[Schema, Type[Schema], Any]
    ) -> Any:
        return PaginatedResponseSchema[response_schema]

    def get_next_link(self, page: Page) -> Optional[str]:
        if not page.has_next():
            return None
        page_number = page.next_page_number()
        return str(page_number)

    def get_previous_link(self, url: str, page: Page) -> Optional[str]:
        if not page.has_previous():
            return None
        page_number = page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)

    def get_page_size(self, max_page: int) -> int:
        if max_page:
            try:
                return _positive_int(max_page, strict=True, cutoff=self.max_page_size)
            except (KeyError, ValueError):
                pass

        return self.max_page


class CustomPagination(pagination.PageNumberPagination):
    """
    Django 페이지네이션 커스터마이징 클래스
    """
    def get_paginated_response(self, data):
        """
        return data 커스터마이징
        """
        _next = self.get_next_link()
        return_data = data
        return_data['response']['page'] = self.page.number
        return_data['response']['next'] = _next.split('page=')[-1] if type(_next) is str else None
        return_data['response']['previous'] = self.get_previous_link()
        return_data['response']['totalCount'] = self.page.paginator.count
        return_data['response']['firstPage'] = 1
        return_data['response']['endPage'] = self.page.paginator.num_pages

        return Response(return_data)

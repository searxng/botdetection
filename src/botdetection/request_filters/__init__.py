from enum import Enum

from flask import Request

import werkzeug

from .._request_info import RequestInfo
from .._request_context import RequestContext
from . import http_accept, http_accept_encoding, http_accept_language, http_connection, http_user_agent, ip_limit


class RequestFilter:  # pylint: disable=too-few-public-methods
    def __call__(
        self,
        context: RequestContext,
        request_info: RequestInfo,
        request: Request,
    ) -> werkzeug.Response | None:
        return None


class PredefinedRequestFilter(Enum):
    HTTP_ACCEPT = http_accept.filter_request
    HTTP_ACCEPT_ENCODING = http_accept_encoding.filter_request
    HTTP_ACCEPT_LANGUAGE = http_accept_language.filter_request
    HTTP_CONNECTION = http_connection.filter_request
    HTTP_USER_AGENT = http_user_agent.filter_request
    IP_LIMIT = ip_limit.filter_request


class RouteFilter(RequestFilter):  # pylint: disable=too-few-public-methods
    def __init__(self, filters: dict[str, list[RequestFilter | PredefinedRequestFilter]]):
        self.filters = filters

    def __call__(
        self,
        context: RequestContext,
        request_info: RequestInfo,
        request: Request,
    ) -> werkzeug.Response | None:
        # FIXME: request.path is not the route
        f_list = self.filters.get(request.path)
        if f_list is None:
            f_list = self.filters.get("*")
        if isinstance(f_list, list):
            for f in f_list:
                if isinstance(f, PredefinedRequestFilter):
                    f = f.value
                val = f(context, request_info, request)
                if val is not None:
                    return val
        return None

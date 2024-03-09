# SPDX-License-Identifier: AGPL-3.0-or-later
# lint: pylint
"""
Method ``http_accept_language``
-------------------------------

The ``http_accept_language`` method evaluates a request as the request of a bot
if the Accept-Language_ header is unset.

.. _Accept-Language:
   https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent

"""
# pylint: disable=unused-argument
from __future__ import annotations

import flask
import werkzeug

from .._helpers import too_many_requests
from .._request_info import RequestInfo
from .._request_context import RequestContext


def filter_request(
    context: RequestContext,
    request_info: RequestInfo,
    request: flask.Request,
) -> werkzeug.Response | None:
    if request.headers.get("Accept-Language", "").strip() == "":
        return too_many_requests(request_info, "missing HTTP header Accept-Language")
    return None

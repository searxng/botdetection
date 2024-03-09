# SPDX-License-Identifier: AGPL-3.0-or-later
# lint: pylint
"""
Method ``http_connection``
--------------------------

The ``http_connection`` method evaluates a request as the request of a bot if
the Connection_ header is set to ``close``.

.. _Connection:
   https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Connection

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
    if request.headers.get("Connection", "").strip() == "close":
        return too_many_requests(request_info, "HTTP header 'Connection=close")
    return None

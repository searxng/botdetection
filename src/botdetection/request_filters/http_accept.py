# SPDX-License-Identifier: AGPL-3.0-or-later
# lint: pylint
"""
Method ``http_accept``
----------------------

The ``http_accept`` method evaluates a request as the request of a bot if the
Accept_ header ..

- did not contain ``text/html``

.. _Accept:
   https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept

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
    if "text/html" not in request.accept_mimetypes:
        return too_many_requests(request_info, "HTTP header Accept did not contain text/html")
    return None

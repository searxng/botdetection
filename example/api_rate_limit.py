from __future__ import annotations

from botdetection import RequestContext, RequestInfo, too_many_requests

import flask
import werkzeug


API_WINDOW = 3600
"""Time (sec) before sliding window for API requests (format != html) expires."""

API_MAX = 4
"""Maximum requests from one IP in the :py:obj:`API_WINDOW`"""


def api_rate_filter_request(
    context: RequestContext,
    request_info: RequestInfo,
    request: flask.Request,
) -> werkzeug.Response | None:
    if request.args.get("format", "html") != "html":
        c = context.redislib.incr_sliding_window("ip_limit.API_WINDOW:" + request_info.network.compressed, API_WINDOW)
        if c > API_MAX:
            return too_many_requests(request_info, "too many request in API_WINDOW")

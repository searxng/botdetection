# SPDX-License-Identifier: AGPL-3.0-or-later
# lint: pylint
"""
Method ``http_user_agent``
--------------------------

The ``http_user_agent`` method evaluates a request as the request of a bot if
the User-Agent_ header is unset or matches the regular expression
:py:obj:`USER_AGENT`.

.. _User-Agent:
   https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent

"""
# pylint: disable=unused-argument

from __future__ import annotations
import re

import flask
import werkzeug

from .._helpers import too_many_requests
from .._request_info import RequestInfo
from .._request_context import RequestContext


USER_AGENT = (
    r"("
    + r"unknown"
    + r"|[Cc][Uu][Rr][Ll]|[wW]get|Scrapy|splash|JavaFX|FeedFetcher|python-requests|Go-http-client|Java|Jakarta|okhttp"
    + r"|HttpClient|Jersey|Python|libwww-perl|Ruby|SynHttpClient|UniversalFeedParser|Googlebot|GoogleImageProxy"
    + r"|bingbot|Baiduspider|yacybot|YandexMobileBot|YandexBot|Yahoo! Slurp|MJ12bot|AhrefsBot|archive.org_bot|msnbot"
    + r"|MJ12bot|SeznamBot|linkdexbot|Netvibes|SMTBot|zgrab|James BOT|Sogou|Abonti|Pixray|Spinn3r|SemrushBot|Exabot"
    + r"|ZmEu|BLEXBot|bitlybot|HeadlessChrome"
    # unmaintained Farside instances
    + r"|"
    + re.escape(r"Mozilla/5.0 (compatible; Farside/0.1.0; +https://farside.link)")
    # other bots and client to block
    + "|.*PetalBot.*"
    + r")"
)
"""Regular expression that matches to User-Agent_ from known *bots*"""

_REGEX = re.compile(USER_AGENT)


def filter_request(
    context: RequestContext,
    request_info: RequestInfo,
    request: flask.Request,
) -> werkzeug.Response | None:
    user_agent = request.headers.get("User-Agent", "unknown")
    if _REGEX.match(user_agent):
        return too_many_requests(request_info, f"bot detected, HTTP header User-Agent: {user_agent}")
    return None

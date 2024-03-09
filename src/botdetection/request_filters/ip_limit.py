# SPDX-License-Identifier: AGPL-3.0-or-later
# lint: pylint
""".. _botdetection.ip_limit:

Method ``ip_limit``
-------------------

The ``ip_limit`` method counts request from an IP in *sliding windows*.  If
there are to many requests in a sliding window, the request is evaluated as a
bot request.  This method requires a redis DB and needs a HTTP X-Forwarded-For_
header.  To take privacy only the hash value of an IP is stored in the redis DB
and at least for a maximum of 10 minutes.

The :py:obj:`.link_token` method can be used to investigate whether a request is
*suspicious*.  To activate the :py:obj:`.link_token` method in the
:py:obj:`.ip_limit` method add the following configuration:

.. code:: toml

   [botdetection.ip_limit]
   link_token = true

If the :py:obj:`.link_token` method is activated and a request is *suspicious*
the request rates are reduced:

- :py:obj:`BURST_MAX` -> :py:obj:`BURST_MAX_SUSPICIOUS`
- :py:obj:`LONG_MAX` -> :py:obj:`LONG_MAX_SUSPICIOUS`

To intercept bots that get their IPs from a range of IPs, there is a
:py:obj:`SUSPICIOUS_IP_WINDOW`.  In this window the suspicious IPs are stored
for a longer time.  IPs stored in this sliding window have a maximum of
:py:obj:`SUSPICIOUS_IP_MAX` accesses before they are blocked.  As soon as the IP
makes a request that is not suspicious, the sliding window for this IP is
dropped.

.. _X-Forwarded-For:
   https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For


Config
~~~~~~

.. code:: toml

   [botdetection.ip_limit]

   # To get unlimited access in a local network, by default link-lokal addresses
   # (networks) are not monitored by the ip_limit
   filter_link_local = false

   # activate link_token method in the ip_limit method
   link_token = false

Implementations
~~~~~~~~~~~~~~~

"""
from __future__ import annotations

from logging import getLogger

import flask
import werkzeug

from .._helpers import too_many_requests
from .._request_info import RequestInfo
from .._request_context import RequestContext


logger = getLogger(__name__)

BURST_WINDOW = 20
"""Time (sec) before sliding window for *burst* requests expires."""

BURST_MAX = 15
"""Maximum requests from one IP in the :py:obj:`BURST_WINDOW`"""

BURST_MAX_SUSPICIOUS = 2
"""Maximum of suspicious requests from one IP in the :py:obj:`BURST_WINDOW`"""

LONG_WINDOW = 600
"""Time (sec) before the longer sliding window expires."""

LONG_MAX = 150
"""Maximum requests from one IP in the :py:obj:`LONG_WINDOW`"""

LONG_MAX_SUSPICIOUS = 10
"""Maximum suspicious requests from one IP in the :py:obj:`LONG_WINDOW`"""

SUSPICIOUS_IP_WINDOW = 3600 * 24 * 30
"""Time (sec) before sliding window for one suspicious IP expires."""

SUSPICIOUS_IP_MAX = 3
"""Maximum requests from one suspicious IP in the :py:obj:`SUSPICIOUS_IP_WINDOW`."""


def filter_request(
    context: RequestContext,
    request_info: RequestInfo,
    request: flask.Request,
) -> werkzeug.Response | None:
    if context.redislib is None or context.link_token is None:
        return filter_request_no_linktoken(context, request_info, request)

    suspicious = context.link_token.is_suspicious(True)

    if not suspicious:
        # this IP is no longer suspicious: release ip again / delete the counter of this IP
        context.redislib.drop_counter("ip_limit.SUSPICIOUS_IP_WINDOW" + request_info.network.compressed)
        return None

    # this IP is suspicious: count requests from this IP
    c = context.redislib.incr_sliding_window(
        "ip_limit.SUSPICIOUS_IP_WINDOW" + request_info.network.compressed, 
        SUSPICIOUS_IP_WINDOW
    )
    if c > SUSPICIOUS_IP_MAX:
        logger.error(
            "BLOCK: too many request from %s in SUSPICIOUS_IP_WINDOW (redirect to /)",
            request_info.network,
        )
        # FIXME: this is SearXNG specific
        return flask.redirect(flask.url_for("index"), code=302)

    c = context.redislib.incr_sliding_window("ip_limit.BURST_WINDOW" + request_info.network.compressed, BURST_WINDOW)
    if c > BURST_MAX_SUSPICIOUS:
        return too_many_requests(request_info, "too many request in BURST_WINDOW (BURST_MAX_SUSPICIOUS)")

    c = context.redislib.incr_sliding_window("ip_limit.LONG_WINDOW" + request_info.network.compressed, LONG_WINDOW)
    if c > LONG_MAX_SUSPICIOUS:
        return too_many_requests(request_info, "too many request in LONG_WINDOW (LONG_MAX_SUSPICIOUS)")

    return None


def filter_request_no_linktoken(
    context: RequestContext,
    request_info: RequestInfo,
    request: flask.Request,  # pylint: disable=unused-argument
) -> werkzeug.Response | None:
    # vanilla limiter without extensions counts BURST_MAX and LONG_MAX
    c = context.redislib.incr_sliding_window("ip_limit.BURST_WINDOW" + request_info.network.compressed, BURST_WINDOW)
    if c > BURST_MAX:
        return too_many_requests(request_info, "too many request in BURST_WINDOW (BURST_MAX)")

    c = context.redislib.incr_sliding_window("ip_limit.LONG_WINDOW" + request_info.network.compressed, LONG_WINDOW)
    if c > LONG_MAX:
        return too_many_requests(request_info, "too many request in LONG_WINDOW (LONG_MAX)")

    return None

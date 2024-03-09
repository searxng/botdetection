# SPDX-License-Identifier: AGPL-3.0-or-later
# lint: pylint
""".. _botdetection src:

Implementations used for bot detection.

"""
from logging import getLogger

from flask import Flask
from redis import Redis

from botdetection.config import Config
from botdetection._redislib import RedisLib
from botdetection._request_info import RequestInfo
from botdetection._botdetection import BotDetection
from botdetection.request_filters import RequestFilter, PredefinedRequestFilter, RouteFilter
from botdetection._helpers import too_many_requests
from botdetection._request_context import RequestContext


__all__ = [
    "install_botdetection",
    "too_many_requests",
    "Config",
    "RequestContext",
    "RequestInfo",
    "RequestFilter",
    "PredefinedRequestFilter",
    "RouteFilter",
    "RedisLib",
]


logger = getLogger(__name__)


def install_botdetection(app: Flask, redis: Redis, config: Config, request_filter: RequestFilter):
    app.botdetection = BotDetection(app, redis, config, request_filter)

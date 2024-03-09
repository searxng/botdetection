# SPDX-License-Identifier: AGPL-3.0-or-later
# lint: pylint

import logging

from ipaddress import ip_address
from flask import Flask, Response, request, render_template_string, make_response

from redis import Redis

from botdetection import _ip_lists
from botdetection._helpers import get_network, get_real_ip
from botdetection.config import Config
from botdetection._redislib import RedisLib
from botdetection._request_info import RequestInfo
from botdetection._request_context import RequestContext
from botdetection.request_filters import RequestFilter
from botdetection._link_token import get_link_token


logger = logging.getLogger(__name__)


class BotDetection:
    def __init__(self, app: Flask, redis: Redis, config: Config, request_filter: RequestFilter):
        self.app = app
        self.config = config
        self.request_filter = request_filter
        prefix = config.botdetection.redis.prefix
        secret = config.botdetection.redis.secret_hash
        self.redislib = RedisLib(redis, prefix, secret) if redis else None
        self.register_jinja_globals()
        self.register_endpoints()
        self.register_before_request()

    def register_before_request(self):
        @self.app.before_request
        def before_request():
            real_ip = ip_address(get_real_ip(self.config, request))
            network = get_network(self.config, real_ip)
            request_info = RequestInfo(real_ip, network)

            link_token = get_link_token(self.redislib, self.config, request_info, request)
            context = RequestContext(self.config, self.redislib, link_token)

            request.botdetection_context = context
            request.botdetection_request_info = request_info

            if request_info.network.is_link_local and not context.config.botdetection.ip_limit.filter_link_local:
                logger.debug(
                    "network %s is link-local -> not monitored by ip_limit method",
                    request_info.network.compressed,
                )
                return None

            # block- & pass- lists
            #
            # 1. The IP of the request is first checked against the pass-list; if the IP
            #    matches an entry in the list, the request is not blocked.
            # 2. If no matching entry is found in the pass-list, then a check is made against
            #    the block list; if the IP matches an entry in the list, the request is
            #    blocked.
            # 3. If the IP is not in either list, the request is not blocked.
            match, msg = _ip_lists.pass_ip(request_info.real_ip, self.config)
            if match:
                logger.warning("PASS %s: matched PASSLIST - %s", request_info.network.compressed, msg)
                return None

            match, msg = _ip_lists.block_ip(request_info.real_ip, self.config)
            if match:
                logger.error("BLOCK %s: matched BLOCKLIST - %s", request_info.network.compressed, msg)
                return make_response(("IP is on BLOCKLIST - %s" % msg, 429))

            # apply the filter(s)
            response = self.request_filter(context, request_info, request)
            if response is not None:
                return response

            # the request is accepted
            return None

    def register_jinja_globals(self):
        template_string = """
        <link rel="stylesheet" href="{{ url_for('client_token', token=link_token) }}" type="text/css" />
        """

        @self.app.context_processor
        def inject_bot_detector():
            def botdetection_html_header():
                link_token = request.botdetection_context.link_token
                if link_token is None:
                    # no link token
                    return ""
                # link_token is initialized
                token = link_token.get_token()
                html = render_template_string(template_string, link_token=token)
                # find the equivalent of flask.Markup and use it
                return html

            return {"botdetection_html_header": botdetection_html_header}

    def register_endpoints(self):
        @self.app.route("/client<token>.css", methods=["GET"])
        def client_token(token=None):
            request.botdetection_context.link_token.ping(token)
            return Response("", mimetype="text/css")

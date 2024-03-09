import os
import logging
import tomllib

from redis import Redis
from flask import Flask, render_template, request
from botdetection import install_botdetection, RouteFilter, Config, PredefinedRequestFilter

from api_rate_limit import api_rate_filter_request


app = Flask("botdetection demo")
logger = logging.getLogger(__name__)


# Registering the middleware
def get_config() -> Config:
    config_raw = {}
    try:
        with open("config.toml", "rb") as f:
            config_raw = tomllib.load(f)
    except IOError:
        print("Error loading config.toml")
        pass
    return Config(**config_raw)


if os.getenv("REDIS", "1") == "1":
    redis = Redis.from_url("redis://localhost:6379/0")
else:
    redis = None


route_filter = RouteFilter(
    {
        "/healthz": [],
        "/search": [
            PredefinedRequestFilter.HTTP_ACCEPT,
            PredefinedRequestFilter.HTTP_ACCEPT_ENCODING,
            PredefinedRequestFilter.HTTP_ACCEPT_LANGUAGE,
            PredefinedRequestFilter.HTTP_USER_AGENT,
            api_rate_filter_request,
            PredefinedRequestFilter.IP_LIMIT,
        ],
        "*": [
            PredefinedRequestFilter.HTTP_USER_AGENT,
        ],
    }
)


if not os.getenv("BOTDETECTION", "1") == "0":
    logger.warning("botdetection is installed")
    install_botdetection(app, redis, get_config(), route_filter)
else:
    logger.warning("botdetection is NOT installed")


@app.route("/")
def index():
    # no need to specify the link_token variable:
    # install_botdetection makes sure it is set in the template

    # get the real_ip if botdetection is enabled
    botdetection_enabled = False
    link_token = False

    botdetection_context = getattr(request, "botdetection_context", None)
    if botdetection_context:
        ip = request.botdetection_request_info.real_ip
        botdetection_enabled = True
        link_token = botdetection_context.link_token is not None
    else:
        ip = request.remote_addr

    return render_template(
        "index.html", 
        ip = ip,
        botdetection_enabled = botdetection_enabled,
        link_token = link_token,
    )


@app.route("/search")
def search():
    return {
        "results": [
            "aa",
            "bb",
            "cc",
        ]
    }


@app.route("/healthz")
def healthz():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run()

# SPDX-License-Identifier: AGPL-3.0-or-later
# lint: pylint

from dataclasses import dataclass

from botdetection.config import Config
from botdetection._redislib import RedisLib
from botdetection._link_token import LinkToken


@dataclass
class RequestContext:
    config: Config
    redislib: RedisLib | None
    link_token: LinkToken | None

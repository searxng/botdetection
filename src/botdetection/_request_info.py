# SPDX-License-Identifier: AGPL-3.0-or-later
# lint: pylint

from dataclasses import dataclass
from ipaddress import (
    IPv4Address,
    IPv6Address,
    IPv4Network,
    IPv6Network,
)


@dataclass
class RequestInfo:
    real_ip: IPv4Address | IPv6Address
    network: IPv4Network | IPv6Network

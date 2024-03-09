# SPDX-License-Identifier: AGPL-3.0-or-later
# lint: pylint
""".. _botdetection.ip_lists:

Method ``ip_lists``
-------------------

The ``ip_lists`` method implements IP :py:obj:`block- <block_ip>` and
:py:obj:`pass-lists <pass_ip>`.


Config
~~~~~~

.. code:: toml

   [botdetection.ip_lists]

   pass_ip = [
    '140.238.172.132', # IPv4 of check.searx.space
    '192.168.0.0/16',  # IPv4 private network
    'fe80::/10'        # IPv6 linklocal
   ]
   block_ip = [
      '93.184.216.34', # IPv4 of example.org
      '257.1.1.1',     # invalid IP --> will be ignored, logged in ERROR class
   ]


Implementations
~~~~~~~~~~~~~~~

"""
# pylint: disable=unused-argument

from __future__ import annotations
from typing import Tuple
from ipaddress import (
    IPv4Address,
    IPv6Address,
    IPv4Network,
    IPv6Network,
)

from botdetection.config import Config
from ._helpers import logger

logger = logger.getChild("ip_limit")


def pass_ip(real_ip: IPv4Address | IPv6Address, cfg: Config) -> Tuple[bool, str]:
    """Checks if the IP on the subnet is in one of the members of the
    ``botdetection.ip_lists.pass_ip`` list.
    """
    return _ip_is_subnet_of_member_in_list(real_ip, cfg.botdetection.ip_lists.pass_ip, "pass_ip")


def block_ip(real_ip: IPv4Address | IPv6Address, cfg: Config) -> Tuple[bool, str]:
    """Checks if the IP on the subnet is in one of the members of the
    ``botdetection.ip_lists.block_ip`` list.
    """

    block, msg = _ip_is_subnet_of_member_in_list(real_ip, cfg.botdetection.ip_lists.block_ip, "block_ip")
    if block:
        msg += " To remove IP from list, please contact the maintainer of the service."
    return block, msg


def _ip_is_subnet_of_member_in_list(
        real_ip: IPv4Address | IPv6Address,
        network_list: list[IPv4Network | IPv6Network],
        list_name: str
    ) -> Tuple[bool, str]:
    for net in network_list:
        if real_ip.version == net.version and real_ip in net:
            return True, f"IP matches {net.compressed} in {list_name}."
    return False, f"IP is not a member of an item in the f{list_name} list"

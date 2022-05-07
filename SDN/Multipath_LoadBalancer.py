"""
Author      : Ramaguru R
Date        : 01 Jan 2022
Description : Multipath Load Balancer
Courtesy    : SDN Multipath Load Balancer Tutorial Video
"""

from ryu import cfg
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.ofproto import ether
from ryu.lib.packet import ipv4
from ryu.lib.ovs import bridge
from ryu.lib.packet import in_proto
from ryu.lib.packet import icmp
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
from ryu.lib import hub
import networkx as nx
from ryu.topology import event, switches
from ryu.topology.api import get_switch, get_link
import random
from time import sleep

INTERVAL = 10
DISCOVERY_INTERVAL = 30

TOPOLOGY_DISCOVERED = 0

ALGO = 1

class Multipath_LoadBalancer(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(Multipath_LoadBalancer, self).__init__(*args, **kwargs)

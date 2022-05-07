# SDN Load Balancer

## Multipath Topology (Image)

<p align="center">
  <img src="/Assets/External/LoadBalancer_Topology.png" alt="Topo" width="500"></img>
</p>

## Mininet Topology (Code)
```
#!/usr/bin/python

# Author: Ramaguru Radhakrishnan
# Updated Date : Jan - 2022
# Network Topology as shown in the YouTube Video on/for Multipath Load Balancing
# Assignment : SDN - RYU Framework - Advanced Networks

from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.topo import Topo

class loadBalancerTopo( Topo ):
    def build( self ):

	print "*** Adding Hosts"

	h1 = self.addHost( 'h1' )
	h2 = self.addHost( 'h2' )
	h3 = self.addHost( 'h3' )
	h4 = self.addHost( 'h4' )

	print "*** Adding Switches"

	s1 = self.addSwitch ( 's1' )
	s2 = self.addSwitch ( 's2' )
	s3 = self.addSwitch ( 's3' )
	s4 = self.addSwitch ( 's4' )
	s5 = self.addSwitch ( 's5' )
	s6 = self.addSwitch ( 's6' )

	print "*** Adding Links"
	print "( h1, s1 ),"
	self.addLink( h1, s1 )
	print "( h2, s1 ),"
	self.addLink( h2, s1 )
	print "( h3, s6 ),"
	self.addLink( h3, s6 )
	print "( h4, s6 ),"
	self.addLink( h4, s6 )
	print "( s1, s2 ),"
	self.addLink( s1, s2 )
	print "( s1, s3 ),"
	self.addLink( s1, s3 )
	print "( s1, s5 ),"
	self.addLink( s1, s5 )
	print "( s2, s6 ),"
	self.addLink( s2, s6 )
	print "( s3, s4 ),"
	self.addLink( s3, s4 )
	print "( s4, s6 ),"
	self.addLink( s4, s6 )
	print "( s5, s6 )"
	self.addLink( s5, s6 )


topos = { 'myNetTopology': ( lambda: loadBalancerTopo() ) }	
```

## RYU SDN Load Balancer [as shown in Video] (Code)

```
#!/usr/bin/python

# Author: Ramaguru Radhakrishnan
# Updated Date : Jan - 2022
# SDN-RYU Load Balancer 
# Reference : Youtube Video as shown in Reference Section. 
# Assignment : SDN - RYU Framework - Advanced Networks

from ryu import app
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

INTERVAL = 10

DISCOVER_INTERVAL = 30
TOPOLOGY_DISCOVERED = 0

ALGO = 2 # [1: Random, 2: Shortest Path First, 3: Round Robin]

class loadBalancer(app_manager.RyuApp):
     OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

     def __init__(self, *args, **kwargs):
        super(loadBalancer, self).__init__(*args, **kwargs)
        
```

### Demo

<p align="center">
	<img src="/Assets/images/LoadBalancer_Simple.png" alt="Load Balancer Demo" width="1000"/>
</p>	

## RYU SDN Load Balancer with Learning (Code)

```
#!/usr/bin/python

# Author: Ramaguru Radhakrishnan
# Updated Date : Jan - 2022
# SDN-RYU Load Balancer 
# Reference : Youtube Video
# Assignment : SDN - RYU Framework - Advanced Networks

import logging
import struct

from ryu import app
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

INTERVAL = 10

DISCOVER_INTERVAL = 30
TOPOLOGY_DISCOVERED = 0

ALGO = 2 # [1: Random, 2: Shortest Path First, 3: Round Robin]

class loadBalancer(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(loadBalancer, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    def add_flow(self, datapath, port, dst, actions):
        ofproto = datapath.ofproto

        match = datapath.ofproto_parser.OFPMatch(in_port=port,
                                                 eth_dst=dst)
        inst = [datapath.ofproto_parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS, actions)]

        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, cookie=0, cookie_mask=0, table_id=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=0, buffer_id=ofproto.OFP_NO_BUFFER,
            out_port=ofproto.OFPP_ANY,
            out_group=ofproto.OFPG_ANY,
            flags=0, match=match, instructions=inst)
        datapath.send_msg(mod)
        
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            self.add_flow(datapath, in_port, dst, actions)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port,
            actions=actions, data=data)
        datapath.send_msg(out)
```

# Reference
- [SDN Training Online. SDN Project - Multipath Load balancing in Software Defined Networking (Mininet, RYU SDN Controller)](https://www.youtube.com/watch?v=XBIR88qnLoA)

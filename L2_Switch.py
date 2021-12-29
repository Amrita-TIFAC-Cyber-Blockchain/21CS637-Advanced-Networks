"""
@author: Ramaguru Radhakrishnan
@Date  : 29.12.2021
@Description : OpenFlow 1.0 - L2 MAC Learning Switch.
@Referred From: https://github.com/faucetsdn/ryu/blob/master/ryu/app/simple_switch.py 
"""

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types

class L2Switch(app_manager.RyuApp):
    # Version is OpenFlow 1.0
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    """
    Initialization Function

    Args:
      **args: command line arguments
      **kwargs: key-value arguments
    """
    def __init__(self, *args, **kwargs):
        super(L2Switch, self).__init__(*args, **kwargs)
        self.mac_table = {}
    
    """
    Adding Flow

    Args:
      datapath: A ryu.controller.controller.Datapath instance of the switch
      in_port: incoming port
      dst: destination Address
      src: source Address
      actions: actions as defined 
    """
    def add_flow(self, datapath, in_port, dst, src, actions):
      
        self.logger.info("Adding Flowing")
        ofproto = datapath.ofproto

        self.logger.info("Matching the Parameter")
        match = datapath.ofproto_parser.OFPMatch(
            in_port=in_port,
            dl_dst=haddr_to_bin(dst), dl_src=haddr_to_bin(src))

        self.logger.info("Data Flow Modification")
        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, match=match, cookie=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=ofproto.OFP_DEFAULT_PRIORITY,
            flags=ofproto.OFPFF_SEND_FLOW_REM, actions=actions)
        datapath.send_msg(mod)

    """
    Packet Handler through Decorator Function.
    
    Args:
      EventOFPPacketIn: 
      MAIN_DISPATCHER: Main Dispatcher
      ev: event
    """    
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        self.logger.info(" Packet Handler")
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        # Check the type for LLDP
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_table.setdefault(dpid, {})

        self.logger.info("Packet in %s %s %s %s", dpid, src, dst, msg.in_port)

        # Learning MAC Address to avoid FLOOD for next instance.
        self.mac_table[dpid][src] = msg.in_port

        if dst in self.mac_table[dpid]:
            out_port = self.mac_table[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            self.add_flow(datapath, msg.in_port, dst, src, actions)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=msg.in_port,
            actions=actions, data=data)
        datapath.send_msg(out)

    """
    Port Status Handler through Decorator Function.
    An event class to notify the port state changes of Datapath instance.
    
    Args:
      EventOFPPortStatus: 
      MAIN_DISPATCHER: Main Dispatcher 
      ev: event
    """  
    @set_ev_cls(ofp_event.EventOFPPortStatus, MAIN_DISPATCHER)
    def _port_status_handler(self, ev):
        msg = ev.msg
        reason = msg.reason
        port_no = msg.desc.port_no

        ofproto = msg.datapath.ofproto
        if reason == ofproto.OFPPR_ADD:
            self.logger.info("Port added %s", port_no)
        elif reason == ofproto.OFPPR_DELETE:
            self.logger.info("Port deleted %s", port_no)
        elif reason == ofproto.OFPPR_MODIFY:
            self.logger.info("Port modified %s", port_no)
        else:
            self.logger.info("Illeagal port state %s %s", port_no, reason)
  

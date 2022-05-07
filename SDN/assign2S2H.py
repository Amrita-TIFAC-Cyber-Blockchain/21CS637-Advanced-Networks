#!/usr/bin/python

# Author: Ramaguru Radhakrishnan
# Network Topology for 2 Switches and 2 Hosts
# Assignment : SDN - RYU Framework - Advanced Networks

from mininet.topo import Topo

class assign2S2H( Topo ):
    def build( self ):
   
        print ("*** Adding Hosts")
        h1 = self.addHost( 'h1', mac = "01:00:00:00:01:00", ip = "10.0.0.2/24" )
        h2 = self.addHost( 'h2', mac = "01:00:00:00:02:00", ip = "10.0.0.3/24" )
        
        print ("*** Adding Switches")
        
        s1 = self.addSwitch ( 's1', listenport = 6634, mac = "00:00:00:00:00:01" )
        s2 = self.addSwitch ( 's2', listenport = 6634, mac = "00:00:00:00:00:02" )
        
        print ("*** Adding Links")
        
        print ("( h1, s1 ),")
        self.addLink( h1, s1 )
        print ("( h2, s2 ),")
        self.addLink( h2, s2 )
        print ("( s1, s2 ),")
        self.addLink( s1, s2 )
     
topos = { 'myNetTopology': ( lambda: assign2S2H() ) }	




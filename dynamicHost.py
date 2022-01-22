#!/usr/bin/python

# Author: Ramaguru Radhakrishnan
# Network Topology for Data Center with Single ToR Switch (Configurable Host)
# Assignment : SDN - RYU Framework - Advanced Networks

from mininet.topo import Topo
import sys

numHosts = 0
class dataRack( Topo ):
    def build( self, nH = 6 ):
            
        self.racks = []
        rootSwitch = self.addSwitch ( 's0' )
        for rackCounter in range( 1, 4 ):
            rack = self.createRack( rackCounter, nH )
            self.racks.append( rack )
            for switch in rack:
                self.addLink( rootSwitch, switch )

    def createRack( self, loc, nH ):
    
        print("Creating Rack", loc)   
        dpid = ( loc * 16 ) + 1
        switch = self.addSwitch( 'r%ss' % loc, dpid='%x' % dpid )

        for hostCounter in range( 1, nH ):
            host = self.addHost( 'r%sh%s' % ( loc, hostCounter ) )
            self.addLink( switch, host )

        # Return list of top-of-rack switches for this rack
        return [switch]       

topos = { 'myNetTopology': ( lambda: dataRack() ) }	
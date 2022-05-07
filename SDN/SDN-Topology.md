# SDN Topology using Mininet

## Single Topology

<p align="center">
  <img src="/Assets/images/SDN_Single_Topology.png" alt="Single" width="800"></img>
</p>

## Linear Topology

<p align="center">
  <img src="/Assets/images/SDN_Linear_Topology.png" alt="Linear" width="800"></img>
</p>

## Link Capability 

```
sudo mn --link tc,bw=10,delay=10ms
```

<p align="center">
  <img src="/Assets/images/SDN_Link_Capability.png" alt="Link Capability" width="800"></img>
</p>

## Design 2-Switches and 2-Hosts 

```
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
```

<p align="center">
  <img src="/Assets/images/SDN_2S2H_Link_Test.png" alt="2S2H" width="800"></img>
</p>

## Design Data Center with Single ToR 

```
#!/usr/bin/python

# Author: Ramaguru Radhakrishnan
# Network Topology for Data Center with Single ToR Switch
# Assignment : SDN - RYU Framework - Advanced Networks

from mininet.topo import Topo

class dataRack( Topo ):
    def build( self ):
            
        self.racks = []
        rootSwitch = self.addSwitch ( 's0' )
        for rackCounter in range( 1, 4 ):
            rack = self.createRack( rackCounter )
            self.racks.append( rack )
            for switch in rack:
                self.addLink( rootSwitch, switch )

    def createRack( self, loc ):
    
        print("Creating Rack", loc)   
        dpid = ( loc * 16 ) + 1
        switch = self.addSwitch( 'r%ss' % loc, dpid='%x' % dpid )

        for hostCounter in range( 1, 4 ):
            host = self.addHost( 'r%sh%s' % ( loc, hostCounter ) )
            self.addLink( switch, host )

        # Return list of top-of-rack switches for this rack
        return [switch]       

topos = { 'myNetTopology': ( lambda: dataRack() ) }	
```

<p align="center">
  <img src="/Assets/images/SDN_DataCenter_Test.png" alt="DataCenter" width="800"></img>
</p>



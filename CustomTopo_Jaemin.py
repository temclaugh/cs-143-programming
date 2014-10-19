from mininet.topo import Topo

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        # Add your logic here ...
        self.fanout = fanout
        core = self.addSwitch('c1')
        edge_count = 1
        host_count = 1
        for a in range(1, fanout+1):
                aswitch = self.addSwitch('a%s' % a)
                self.addLink(aggswitch, c1,  **linkopts1)
                for e in range (1, fanout+1):
                        eswitch = self.addSwitch('e%s' % edge_count)
                        edge_count += 1
                        self.addLink(eswitch, aswitch,  **linkopts2)
                        for h in range (1, fanout+1):
                                host = self.addHost('h%s' % host_count)
                                host_count += 1
                                self.addLink(host, eswitch, **linkopts3)
#Linkopts
linkopts1 = dict(bw=10, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
linkopts2 = dict(bw=10, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
linkopts3 = dict(bw=10, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)        
                    
topos = { 'custom': ( lambda: CustomTopo() ) }
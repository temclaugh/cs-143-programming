from mininet.topo import Topo

class Q9Topo(Topo):
    def __init__(self, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        # add switches
        s11 = self.addSwitch('s11')
        s12 = self.addSwitch('s12')
        s14 = self.addSwitch('s14')
        s16 = self.addSwitch('s16')
        s18 = self.addSwitch('s18')

        # add hosts
        h13 = self.addHost('h13')
        h15 = self.addHost('h15')    
        h17 = self.addHost('h17')   
        h19 = self.addHost('h19')

        # add links between switch and link
       	self.addLink(s12, h13, **linkopts)
       	self.addLink(s14, h15, **linkopts)
       	self.addLink(s16, h17, **linkopts)
       	self.addLink(s18, h19, **linkopts)

       	# add links between switches
       	self.addLink(s11, s12, **linkopts_g)
       	self.addLink(s12, s14, **linkopts_h)
       	self.addLink(s14, s16, **linkopts_i)
       	self.addLink(s16, s18, **linkopts_j)
       	self.addLink(s18, s11, **linkopts_k)
       	self.addLink(s12, s18, **linkopts_l)
       	self.addLink(s12, s16, **linkopts_m)
       	self.addLink(s14, s18, **linkopts_n)

linkopts_g = dict(bw=10, delay='10ms', loss=0, max_queue_size=1000, use_htb=True)
linkopts_h = dict(bw=10, delay='50ms', loss=0, max_queue_size=1000, use_htb=True)
linkopts_i = dict(bw=10, delay='10ms', loss=0, max_queue_size=1000, use_htb=True)
linkopts_j = dict(bw=10, delay='30ms', loss=0, max_queue_size=1000, use_htb=True)
linkopts_k = dict(bw=10, delay='30ms', loss=0, max_queue_size=1000, use_htb=True)
linkopts_l = dict(bw=10, delay='10ms', loss=0, max_queue_size=1000, use_htb=True)
linkopts_m = dict(bw=10, delay='100ms', loss=0, max_queue_size=1000, use_htb=True)
linkopts_n = dict(bw=10, delay='20ms', loss=0, max_queue_size=1000, use_htb=True)
linkopts = dict(bw=10, delay='0ms', loss=0, max_queue_size=1000, use_htb=True)

                    
topos = { 'custom': ( lambda: Q9Topo() ) }
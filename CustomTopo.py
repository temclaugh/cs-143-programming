from mininet.topo import Topo

class CustomTopo(Topo):
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
	print dir(Topo)
    	Topo.__init__(self, **opts)


linkopts1 = dict(bw=10, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
linkopts2 = dict(bw=10, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)
linkopts3 = dict(bw=10, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)

topos = {'custom': (lambda: CustomTopo(linkopts1, linkopts2, linkopts3))}

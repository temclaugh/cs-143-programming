from collections import Counter

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class CustomTopo(Topo):
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
    	Topo.__init__(self, **opts)
    	self.fanout = fanout
        linkopts = [linkopts1, linkopts2, linkopts3]
        aggregateSwitches = []
        edgeSwitches = []
        hosts = []
        core = self.addSwitch('c1')
        levels = {'c' : 'a', 'a' : 'e', 'e' : 'h'}
        q = [(core, 'c', 0)]
        counts = Counter()

        # breadth-first traversal
        while q != []:
            parent, nodeType, level = q.pop(0)
            childNodeType = levels[nodeType]
            for i in irange(1, fanout):
                counts[childNodeType] += 1
                identifier = '%s%d' % (childNodeType, counts[childNodeType])
                if childNodeType == 'h':
                    child = self.addHost(identifier, cpu=.5/fanout)
                else:
                    child = self.addSwitch(identifier)
                self.addLink(parent, child, **(linkopts[level]))
                if childNodeType != 'h':
                    q.append((child, childNodeType, level + 1))

linkopts1 = dict(bw=10, delay='5ms', loss=0, max_queue_size=1000, use_htb=True)
linkopts2 = dict(bw=10, delay='5ms', loss=0, max_queue_size=1000, use_htb=True)
linkopts3 = dict(bw=10, delay='5ms', loss=0, max_queue_size=1000, use_htb=True)

topos = {'custom': (lambda: CustomTopo(linkopts1, linkopts2, linkopts3))}

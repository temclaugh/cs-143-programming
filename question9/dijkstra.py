from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from pox.lib.addresses import IPAddr
from collections import namedtuple
from collections import defaultdict
from copy import deepcopy
import os
import csv

log = core.getLogger()
delayFile = "%s/pox/pox/misc/delay.csv" % os.environ[ 'HOME' ]

hosts = {'h13': 's12', 'h15': 's14', 'h17': 's16', 'h19': 's18'}

# switches of links given in delay.csv
linkNames = {
    'g': ('s11', 's12'),
    'h': ('s12', 's14'),
    'i': ('s14', 's16'),
    'j': ('s16', 's18'),
    'k': ('s11', 's18'),
    'l': ('s12', 's18'),
    'm': ('s12', 's16'),
    'n': ('s14', 's18'),
}

# the port number for a given destination
portMappings = {
    's11': {'s12': 1, 's18': 2},
    's12': {'h13': 1, 's11': 2, 's14': 3, 's18': 4, 's16': 5},
    's14': {'h15': 1, 's12': 2, 's16': 3, 's18': 4},
    's16': {'h17': 1, 's14': 2, 's18': 3, 's12': 4},
    's18': {'h19': 1, 's16': 2, 's11': 3, 's12': 4, 's14': 5},
    'h13': {'s12': 0},
    'h15': {'s14': 0},
    'h17': {'s16': 0},
    'h19': {'s18': 0},
}

hostMappings = {
    'h13': ('10.0.0.1', '00:00:00:00:00:01'),
    'h15': ('10.0.0.2', '00:00:00:00:00:02'),
    'h17': ('10.0.0.3', '00:00:00:00:00:03'),
    'h19': ('10.0.0.4', '00:00:00:00:00:04'),
}

class Dijkstra(EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Dijkstra Module")


        self.delays = {}
        self.switches = set()
	self.neighbors = defaultdict(set)
        with open(delayFile, 'r') as csvfile:
            links = csv.reader(csvfile, delimiter=',')
            links.next() # skip first line: "link,delay"
            for linkName, delay in links:
                s1, s2 = linkNames[linkName]
                self.delays[(s1, s2)] = int(delay)
		self.delays[(s2, s1)] = int(delay)
                self.switches.add(s1)
                self.switches.add(s2)
		self.neighbors[s1].add(s2)
		self.neighbors[s2].add(s1)


    def _dijkstra(self, source):
	distances = defaultdict(lambda: float('inf'))
	distances[source] = 0
	previous = {}
	unseen = deepcopy(self.switches)
	while unseen != set():
	    minDist = float('inf')
	    u = min(unseen, key=lambda x: distances[x])
	    unseen.remove(u)
	    for v in self.neighbors[u]:
                alt = distances[u] + self.delays[(u, v)]
		if alt <= distances[v]:
		    distances[v] = alt
		    previous[v] = u

	return distances, previous

    def _getPortMapping(self, source):
	distances, previous = self._dijkstra(source)
	ports = {}
	for destHost, destSwitch in hosts.iteritems():
	    if source == destSwitch:
	        ports[destHost] = portMappings[source][destHost]
		continue
	    while source != previous[destSwitch]:
                destSwitch = previous[destSwitch]
	    ports[destHost] = portMappings[source][destSwitch]

    	return ports

    def _handle_ConnectionUp(self, event):
        switch = 's' + str(event.dpid)
        ports = self._getPortMapping(switch)

	for host, (ip, mac) in hostMappings.iteritems():
	    port = ports[host]
	    print switch, host, ip, mac, port

            msg_mac = of.ofp_flow_mod()
            msg_mac.match.dl_dst = EthAddr(mac)
            msg_mac.actions.append(of.ofp_action_output(port=port))
	    event.connection.send(msg_mac)

            msg_ip = of.ofp_flow_mod()
            msg_ip.match.nw_dst = IPAddr(ip)
	    msg_ip.match.dl_type = 2054
            msg_ip.actions.append(of.ofp_action_output(port=port))
	    event.connection.send(msg_ip)

        log.debug("Dijkstra installed on %s", dpidToStr(event.dpid))

def launch():
    '''
    Starting the Dijkstra module
    '''
    core.registerNew(Dijkstra)


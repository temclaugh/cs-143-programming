from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
from collections import defaultdict
import os
import csv

log = core.getLogger()
delayFile = "delay.csv"

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

macMappings = {
    '00:00:00:00:00:01': 'h13',
    '00:00:00:00:00:02': 'h15',
    '00:00:00:00:00:04': 'h19',
    '00:00:00:00:00:03': 'h17',
}

hardCodedPorts = {
    's11': {'h13': 1, 'h15': 1, 'h17': 2, 'h19': 2},
    's12': {'h13': 1, 'h15': 3, 'h17': 5, 'h19': 4},
    's14': {'h13': 2, 'h15': 1, 'h17': 3, 'h19': 4},
    's16': {'h13': 4, 'h15': 2, 'h17': 1, 'h19': 3},
    's18': {'h13': 4, 'h15': 5, 'h17': 2, 'h19': 1},
}

class Dijkstra(EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Dijkstra Module")


        self.delays = {}
        self.switches = set()
        with open(delayFile, 'r') as csvfile:
            links = csv.reader(csvfile, delimiter=',')
            links.next() # skip first line: "link,delay"
            for linkName, delay in links:
                s1, s2 = linkNames[linkName]
                self.delays[(s1, s2)] = int(delay)
                self.switches.add(s1)
                self.switches.add(s2)

    def _dijkstra(self, source):
        distances = {source: 0}
        previous = defaultdict(None)
        unseen = set()
        for switch in self.switches:
            if switch != source:
                distances[switch] = float("inf")
                previous[switch] = None
            unseen.add(switch)

        # create neighbor table
        neighbors = defaultdict(set)
        for s1, s2 in self.delays.iterkeys():
            neighbors[s1].add(s2)
            neighbors[s2].add(s1)

        # run dijktras
        while unseen != set():
            u = None
            minDist = float("inf")
            for switch in unseen:
                if distances[switch] <= minDist:
                    minDist = distances[switch]
                    u = switch
            unseen.remove(switch)

            for neighbor in neighbors[u]:
                a = min(u, neighbor)
                b = max(u, neighbor)
                alt = distances[u] + self.delays[(a, b)]
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = u

	print previous
        return previous


    # returns a mapping from mac address to port numbers
    def _getPortMapping(self, source):
        previous = self._dijkstra(source)
        routingTable = {}
        for switch in self.switches:
	    if switch == source:
		continue
	    print "finding mapping from", switch, "to", source
	    try:
                destination = previous[switch]
                while previous[destination] != switch:
                    destination = previous[destination]
                routingTable[portMapping[source]][switch] = destination
	    except:
	        print source
		print destination
		print previous
		raise KeyError
        return routingTable

    def _handle_ConnectionUp(self, event):
        switch = 's' + str(event.dpid)
        #routingTable = self._getPortMapping(switch)

        for macAddress, hostName in macMappings.iteritems():
            #if portMappings[switch].has_key(hostName):
                #port = portMappings[switch][hostName]
            #else:
                #port = routingTable[macAddress]
	    port = hardCodedPorts[switch][hostName]
	    print ">>>>", switch, hostName, port
            msg = of.ofp_flow_mod()
            msg.match.dl_dst = EthAddr(macAddress)
            msg.actions.append(of.ofp_action_output(port=port))
            event.connection.send(msg)

        msg = of.ofp_flow_mod()
        msg.match.dl_dst = EthAddr('FF:FF:FF:FF:FF:FF')
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)

        log.debug("Dijkstra installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Dijkstra module
    '''
    core.registerNew(Dijkstra)

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
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
    's16': {'h17': 1, 's14': 2, 's18': 3, 's12': 4,}
    's18': {'h19': 1, 's16': 2, 's11': 3, 's12': 4, 's14': 5,},
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

# given a destination, produces the port number to get there
routingTable = defaultdict(lamdba x: 0)

class Dijkstra(EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Dijkstra Module")


        self.delays = {}
        self.switches = set()
        with open(delayFile, 'r') as csvfile:
            links = csv.reader(csvfile, delimiter=',')
            linkes.next() # skip first line: "link,delay"
            for linkName, delay in links:
                s1, s2 = linkNames[linkName]
                self.delays[(s1, s2)] = int(delay)
                switches.add(s1)
                switches.add(s2)

        def _dijkstra(self, source):
            distances = {source: 0}
            previous = defaultdict(None)
            unseen = set()
            for switch in switches:
                if switch != source:
                    distances[switch] = float("inf")
                    previous[switch] = None
                unseen.add(switch)

            # create neighbor table
            neighbors = defaultdict(set)
            for s1, s2 in delays.iterkeys():
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
                    alt = distances[u] + delays[(a, b)]
                    if alt < distances[neighbor]:
                        distances[neighbor] = alt
                        previous[neighbor] = u

            return previous


    # returns a mapping from mac address to port numbers
    def _getPortMapping(self, source):
        previous = self._dijkstra(switch)
        routingTable = {}
        for switch in self.switches:
            destination = previous[switch]
            while previous[destination] != switch:
                destination = previous[destination]
            routingTable[portMapping[source]][switch] = destination
        return routingTable

    def _handle_ConnectionUp(self, event):
        switch = 's' + dpidToStr(event.dpid)
        routingTable = _getPortMapping(switch)

        for macAddress, hostName in macMappings.iteritems():
            if portMappings[switch].has_key(hostName):
                port = portMappings[switch][hostName]
            else:
                port = routingTable[macAddress]
            msg = of.ofp_flow.mod()
            msg.match.dl_dst = EthAddr(macAddress)
            msg.actions.append(of.ofp_action_output(port=port))
            event.connection.send(msg)

        log.debug("Dijkstra installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Dijkstra module
    '''
    core.registerNew(Dijkstra)

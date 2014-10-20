import csv
from collections import defaultdict
delayFile = "delay.csv"

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

def dijkstra(switches, delays, source):
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

def route(source, destination, previous):
    while previous[destination] != source:
        destination = previous[destination]
    return destination


class Dijkstra():

    def __init__(self):
        self.delays = {}
        switches = set()
        with open(delayFile, "r") as csvfile:
            links = csv.reader(csvfile, delimiter=",")
            links.next() # skip first line "link,delay"
            for linkName, delay in links:
                s1, s2 = linkNames[linkName]
                self.delays[(s1, s2)] = int(delay)
                switches.add(s1)
                switches.add(s2)
        distances = {}
        for switch in switches:
            previous = dijkstra(switches, self.delays, switch)
            print "routing from", switch
            for switch_ in switches:
                if switch == switch_:
                    continue
                print "    to", switch_, "go to", route(switch, switch_, previous)
Dijkstra()

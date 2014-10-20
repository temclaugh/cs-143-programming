from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''
rules = []

# Read rules from csv into an array
with open(policyFile) as f:
	content = f.readlines()
	for idx, line in enumerate(content):
		if idx == 0:
			properties = line.split(",")
			properties[-1] = properties[-1].strip()
		else:
			linearray = line.split(",")
			linearray[-1] = linearray[-1].strip()
			# Incomplete rules
			if len(linearray) != len(properties):
				continue
			rules.append({})
			for prop in properties:
				rules[idx-1][prop] = linearray[properties.index(prop)]



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):    
        
	
	for idx,rule in enumerate(rules):
		log.debug("Installing rule %i", rule['id'] )
		msg = of.ofp_flow_mod()
		
		# Avoid Conflicts
		msg.priority = 1000 * idx
		
		msg.match.dl_src = EthAddr(rule['mac_0'])
		msg.match.dl_dst =  EthAddr(rule['mac_1'])
		
		# Do nothing (DROP)
		msg.actions = []	
		
		#Send message to switch
		event.connection.send(msg)
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)

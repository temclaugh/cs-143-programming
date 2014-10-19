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
with open(policyFile) as f:
	content = f.readlines()
	for idx, line in enumerate(content):
		if idx == 0:
			properties = line.split(",")
			properties[-1] = properties[-1].strip()
		else:
			rules.append({})
			linearray = line.split(",")
			linearray[-1] = linearray[-1].strip()
			for prop in properties:
				rules[idx-1][prop] = linearray[properties.index(prop)]



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
        
	
	for rule in rules:
		log.debug("Installing rule from %s to %s", rule['mac_0'], rule['mac_1'] )
	
		msg = of.ofp_flow_mod()
		msg.priority = 100
		msg.match.dl_src = rule['mac_0']
		msg.match.dl_dst =  rule['mac_1']
		msg.actions.append(of.ofp_action_output(port = of.OFPP_NONE))	
		#Send message to switch
		event.connection.send(msg)
    
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)

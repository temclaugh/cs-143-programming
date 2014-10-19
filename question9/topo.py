from mininet.topo import Topo

class Q9Topo(Topo):
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

      	
        s11 = 11
        s12 = 12
        s13 = 13
        s14 = 14
        h15 = 15
        s16 = 16
        h17 = 17
        s18 = 18
        h19 = 19

        self.add node(s1, Node(is switch = True))
		self.add node(s2, Node(is switch = True))
		self.add node(s3, Node(is switch = True))
		self.add node(s4, Node(is switch = True))
		self.add node(s5, Node(is switch = True))
		self.add node(h6, Node(is switch = False))
		self.add node(h7, Node(is switch = False))
		self.add node(h8, Node(is switch = False))
		self.add node(h9, Node(is switch = False))
		self.add node(h10, Node(is switch = False))
		# link delays
		a = 100
		b = 50
		c = 20
		d = 5
		e = 5
		f = 10
		# add edges
		self.add edge(s1, h6, delay = a)
		self.add edge(s1, h7)
		self.add edge(s1, s2, delay = b)  # host and switches IDs
        # we add hosts according to the IDs
       	self.add edge(s2, s3, delay = c)
		self.add edge(s3, h8, delay = e)
		self.add edge(s3, s4, delay = d)
		self.add edge(s4, h10, delay = f)
		self.add edge(s2, s5)
		self.add edge(s5, h9)

        # Add your logic here ...
        
                    
topos = { 'custom': ( lambda: Q9Topo() ) }
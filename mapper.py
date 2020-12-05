class Route:
	def __init__(self, network, via, moi, metric):
		self.network = network
		self.via = via
		self.moi = moi
		self.metric = metric

	def getRoute(self):
		return self.network+"\n(Metric: "+self.metric+")"

	def getVia(self):
		return self.via

	def getMoi(self):
		return self.moi

	def __str__(self):
		return "route: [Network: "+self.network+", Via: " + self.via+"]"

def getRoutes(babelArray, myID):
	routes = []
	
	for line in babelArray:
		elements = line.split(" ")
		
		if elements[0] == "add" and elements[1] == "route" and elements[8] == "yes":
			routes.append(Route(elements[4], elements[10], myID, elements[12]))

	return routes


def babelCollect(ip, port):
	import subprocess
	babelData = subprocess.getoutput("bash -c \"echo dump | ncat "+ip+" "+port+" --no-shutdown -i 1\"")

	"Only valid ncat one would have this (as the connection succeeded and we got a babel daemon response)"
	if "my-id" in babelData:
		babelArray = babelData.split("\n")
		babelID = babelArray[3].split(" ")[1]
		print("My ID: "+babelID)

		routes = getRoutes(babelArray, babelID)
		return routes

	return None

def collectAllRoutes(peersFile):
	file = open(peersFile, "r")
	data = file.read()

	allRoutes = []

	for peer in  data.split("\n"):
		nodeIP = peer.split(" ")[0]
		nodePort = peer.split(" ")[1]

		routes = babelCollect(nodeIP, nodePort)
		if routes != None:
			for route in routes:
				allRoutes.append(route)

	return allRoutes

def makeGraph(peersFile):
	routes = collectAllRoutes(peersFile)
	print("Collected "+str(len(routes))+" routes")

	graph="graph networkMap {"

	"Add some spacing between nodes (vertically)"
	graph+="graph [ranksep=\"2\"]"

	for route in routes:
		graph += "\""+route.getMoi()+"\" -- \""+route.getVia() +"\" [label=\""+route.getRoute()+"\"]"

	graph+="}"

	"Write out graph to disk"
	file = open("thing.dot","w")
	file.write(graph)
	file.close()

	import os
	os.system("cat thing.dot | dot -Tpng -o graph.png")

makeGraph("peers.list")

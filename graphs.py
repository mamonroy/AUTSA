import networkx as nx 
import matplotlib.pyplot as plt

class Graphs:
	GraphArr = []
	G = nx.DiGraph()
	# G = nx.DiGraph.reverse(True)

	def addEdges(self,edges):
		self.GraphArr.append(edges)

	def draw(self):
		self.G.add_edges_from(self.GraphArr)
		self.G = self.G.reverse(True)
		pos = nx.spring_layout(self.G)
		nx.draw_networkx_nodes(self.G, pos, node_size=500)
		nx.draw_networkx_edges(self.G, pos, edgelist = self.G.edges(), edge_color='black')
		nx.draw_networkx_labels(self.G, pos)
		plt.show()
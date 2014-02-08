

class Graph:
	def __init__(self, edges, length):
		self.edges = edges
		self.length = length
		self.rank_dict = {k:[] for k in xrange(self.length)}
		
		self.vertices = []
		edge_dict = {k:[] for k in xrange(length)}
		for e in edges:
			edge_dict[e[0]].append([e[1], 1])
			edge_dict[e[1]].append([e[0], -1])
		for k in edge_dict:
			self.vertices.append(self.Vertex(edge_dict[k], k))


	def set_rank_dict(self):
		for v in self.vertices:
			if v.rank < 0:
				print "Error - not normalized."
				return
			self.rank_dict[v.rank].append(v)
		# Remove empty ranks?

	def insert_vertex(self, edges):
		new_v = self.Vertex(edges, self.length)
		self.vertices.append(new_v)
		self.length += 1
		return new_v

	class Vertex:
		def __init__(self, edges, index):
			self.edges = edges
			self.index = index
			self.rank = None
			self.x = None
			self.y = None
			self.is_tmp = False
		
		def set_x(self, x): self.x = x

		def set_y(self, y): self.y = y

		def set_is_tmp(self): self.is_tmp = True


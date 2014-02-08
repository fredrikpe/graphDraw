

import rank
import ordering
import position

def graph_draw(graph):
	rank.rank(graph)
	print "done rank"
	tmp_graph = ordering.ordering(graph)
	print "done ordering"
	position.position(tmp_graph)
	print "done position"

	return tmp_graph
	#make_splines()


if __name__ == "__main__":
	l = 4
	edges = [[0, 1], [1, 2], [2, 3], [3, 0]]

	g = graph.Graph(edges, l)
	for v in g.vertices:
		print v.edges

	rank.rank(g)

	for v in g.vertices:
		print v.rank

	ordering.elim_long_edges(g)
	print "elim_longEdges"
	for v in g.vertices:
		print v.edges

	for v in g.vertices:
		print v.rank
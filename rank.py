




# Assuming unweighted graph, build spanning tree (dfs) and rank thereafter
def rank(graph):
    visited = []
    next = []
    cur = graph.vertices[0]
    visited.append(0)
    lenght = len(graph.vertices)
    cur.rank = lenght / 4

    while len(visited) < lenght:
        for edge in cur.edges:
            if edge[0] not in visited:
                visited.append(edge[0])
                graph.vertices[edge[0]].rank = cur.rank + edge[1]
                if edge[0] not in next:
                    next.append(edge[0])
        cur = graph.vertices[next.pop()]
    normalize(graph)


def normalize(graph):
    min_rank = graph.vertices[0].rank
    for v in graph.vertices:
        if v.rank < min_rank:
            min_rank = v.rank
    dif = -min_rank
    for v in graph.vertices:
        v.rank += dif


'''
def rank():
	feasible_tree()
	e = leave_edge()
	while e is not None:
		f = enter_edge(e)
		exchange(e,f)
	normalize()
	balance()


def leave_edge():
	pass

def feasible_tree():
	init_rank()
	while tight_tree() < |V|:
		e = # a non-tree edge incident on the tree with a minimal amount of slack
		delta = slack(e)
		if incident node is e.head:
			delta = -delta
		for v in Tree:
			v.rank = v.rank + delta
	init_cutvalues()
'''

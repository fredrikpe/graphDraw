
import copy


def ordering(graph, max_iterations=24):
    tmp_graph = copy.deepcopy(graph)
    elim_long_edges(tmp_graph)
    merge_multi_edges(tmp_graph)

    tmp_graph.set_rank_dict()

    order = tmp_graph.rank_dict
    best = order
    for i in xrange(max_iterations):
        wmedian(order, i, tmp_graph.length)
        transpose(order, i % 2 == 0)
        if crossing(order) < crossing(best):
            best = order
    for i in xrange(max_iterations):
        wmedian(order, max_iterations - i - 1, tmp_graph.length)
        transpose(order, i % 2 == 0)
        if crossing(order) < crossing(best):
            best = order
    tmp_graph.rank_dict = best

    #remove_tmp_edges(tmp_graph)
    return tmp_graph


def remove_tmp_edges(graph):
    b = True
    while b:
        b = False
        for v in graph.vertices:
            if v.is_tmp:
                graph.vertices[v.edges[0][0]].edges.append([v.edges[1][0], 1])
                graph.vertices[v.edges[1][0]].edges.append([v.edges[0][0], -1])
                graph.vertices.remove(v)
                b = True


def elim_long_edges(graph):
    for e in graph.edges:
        v1 = graph.vertices[e[0]]
        v2 = graph.vertices[e[1]]
        if abs(v1.rank - v2.rank) > 1:
            graph.edges.remove(e)
            v1.edges.remove([e[1], 1])
            v2.edges.remove([e[0], -1])
            cur = v1
            for i in xrange(1, abs(v1.rank - v2.rank)):
                index = len(graph.vertices)
                new_edges = [[cur.index, -1]]
                if i < abs(v1.rank - v2.rank) - 1:
                    new_edges.append([index + 1, 1])
                else:
                    new_edges.append([e[1], 1])
                if i == 1:
                    v1.edges.append([index, 1])
                elif i == abs(v1.rank - v2.rank) - 1:
                    v2.edges.append([index, -1])
                new_v = graph.insert_vertex(new_edges)
                new_v.set_is_tmp()
                new_rank = min([v1.rank, v2.rank]) + i
                new_v.rank = new_rank
                graph.rank_dict[new_rank].append(new_v)
                cur = graph.vertices[-1]


def merge_multi_edges(graph):
    '''
    for e in graph.edges:
            if e[0] == e[1]:
                    graph.edges.remove(e)
                    graph.vertices[e[0]].edges.remove([e[0], 1])
            for d in graph.edges:
                    if d[0] == e[1] and d[1] == e[0]:
                            graph.edges.remove(d)
    '''
    pass


def init_order(graph):
    order = [[v for v in graph.vertices if v.rank == n]
             for n in xrange(graph.length)]
    for i in xrange(graph.length):
        if order[i] == []:
            return order[:i]
    return order


def wmedian(order, i, length):
    median = [0 for _ in xrange(length)]
    max_rank = len(order) - 1
    if i % 2 == 0:
        for r in xrange(1, max_rank + 1):
            i = 0
            for v in order[r]:
                median[i] = median_value(v, order[r - 1])
                i += 1
            sort(order[r], median)
    else:
        for r in xrange(1, max_rank + 1):
            i = 0
            for v in order[max_rank - r]:
                median[i] = median_value(v, order[max_rank - r + 1])
                i += 1

            sort(order[max_rank - r], median)


def sort(rank, median):
    tmp_list = [[median[i], rank[i]] for i in xrange(len(rank))]
    selection_sort(tmp_list)
    rank = [tmp_list[i][1] for i in xrange(len(rank))]


def selection_sort(list2):
    for i in range(0, len(list2)):
        minimum = i
        for j in range(i + 1, len(list2)):
            if list2[j][0] <= list2[minimum][0]:
                minimum = j
        list2[i][0], list2[minimum][0] = list2[minimum][0], list2[i][0]  # swap


def median_value(v, adj_rank):
    P = adj_positions(v, adj_rank)
    len_P = len(P)
    m = len_P / 2
    if len_P == 0:
        return -1.0
    elif len_P % 2 == 1:
        return P[m]
    elif len_P == 2:
        return (P[0] + P[1]) / 2.0
    else:
        left = P[m - 1] - P[0] + 0.0
        right = P[len_P - 1] - P[m]
        return (P[m - 1] * right + P[m] * left) / (left + right)


def adj_positions(v, adj_rank):
    P = []
    for i in xrange(len(adj_rank)):
        for e in v.edges:
            if e[0] == adj_rank[i].index:
                P.append(i)
                break
    return P


def transpose(order, c):
    max_rank = len(order) - 1
    improved = True
    while improved:
        improved = False
        for j in xrange(max_rank + 1):
            for i in xrange(len(order[j]) - 1):
                v = order[j][i]
                w = order[j][i + 1]
                a, b = crossing(order, j, i, i + 1)
                if a:
                    improved = True
                    exchange(order, j, i, i + 1)


def exchange(order, j, v_i, w_i):
    order[j][w_i],  order[j][v_i] = order[j][v_i], order[j][w_i]


def crossing(order, rank_index=None, v_i=None, w_i=None):
    crossings = 0
    if rank_index is None:
        cur = order[0]
        for i in xrange(1, len(order)):
            crossings += sum_crossing(order, i, cur)
            cur = order[i]
        return crossings
    else:
        tmp_order = copy.deepcopy(order)
        exchange(tmp_order, rank_index, v_i, w_i)
        cross1 = 0
        cross2 = 0
        if rank_index > 0:
            cur = order[rank_index - 1]
            cross1 += sum_crossing(order, rank_index - 1, cur)

            cur = tmp_order[rank_index - 1]
            cross2 += sum_crossing(tmp_order, rank_index - 1, cur)

        if rank_index < len(order) - 1:
            cur = order[rank_index]
            cross1 += sum_crossing(order, rank_index + 1, cur)

            cur = tmp_order[rank_index]
            cross2 += sum_crossing(tmp_order, rank_index + 1, cur)
        return cross2 < cross1, cross2 == cross1


def sum_crossing(order, rank_index, cur):
    crossings = 0
    ps = [adj_positions(v, order[rank_index]) for v in cur]
    if len(ps) > 0:
        cur_P = ps[0]
        for j in xrange(1, len(ps)):
            for n in ps[j]:
                cro = [1 for m in cur_P if n < m]
                crossings += sum(cro)
    return crossings


if __name__ == "__main__":
    import graph
    import rank


    length = 8
    edges = [[0, 1], [0, 2], [1, 4], [1, 5], [2, 3], [4, 6], [3, 7], [5, 6]]

    g = graph.Graph(edges, length)

    rank.rank(g)

    order = ordering(g)

    print crossing(order)

    for o in order:
        s = "Rank: "
        for v in o:
            s += " " + str(v.index) + " "
        print s

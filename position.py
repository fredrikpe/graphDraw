

def position(graph):
    i = 0
    for k in graph.rank_dict:
        i = 0
        for v in graph.rank_dict[k]:
            print 100*k, 100*i
            v.set_x(100*k)
            v.set_y(100*i)
            i += 1

  
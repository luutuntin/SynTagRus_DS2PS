#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SynTagRus DS Projectivity Module
alexluu@brandeis.edu

Demo:
>>> 
Number of projective sents:  3636
Number of non-projective sents:  397
Indexes of these sentences:  [13, 51, 72, 73, 95, 121, 135,
183, 203, 302, 310, 324, 340, 341, 342, 345, 351, 359, 385,
392, 395, 429, 445, 459, 490, 493, 494, 510, 512, 526, 561,
565, 568, 570, 573, 581, 597, 603, 604, 605, 615, 616, 618,
623, 630, 646, 651, 674, 693, 710, 718, 725, 726, 727, 737,
750, 751, 754, 777, 789, 792, 812, 862, 870, 871, 931, 985,
989, 999, 1002, 1041, 1046, 1048, 1074, 1077, 1082, 1103,
1104, 1120, 1123, 1128, 1131, 1136, 1146, 1153, 1156, 1160,
1191, 1198, 1200, 1202, 1206, 1212, 1237, 1238, 1244, 1253,
1261, 1263, 1275, 1289, 1305, 1309, 1314, 1317, 1326, 1337,
1351, 1354, 1368, 1378, 1386, 1388, 1400, 1406, 1413, 1415,
1423, 1466, 1473, 1476, 1484, 1527, 1528, 1543, 1547, 1554,
1569, 1577, 1591, 1598, 1609, 1611, 1615, 1623, 1667, 1668,
1671, 1697, 1703, 1707, 1709, 1710, 1718, 1719, 1743, 1749,
1774, 1814, 1826, 1828, 1832, 1836, 1842, 1859, 1862, 1870,
1871, 1873, 1905, 1925, 1939, 1940, 1941, 1946, 1950, 1970,
1975, 1994, 1998, 2003, 2008, 2027, 2031, 2032, 2037, 2052,
2069, 2091, 2099, 2104, 2120, 2125, 2142, 2143, 2145, 2158,
2163, 2169, 2173, 2180, 2181, 2182, 2188, 2190, 2192, 2223,
2228, 2236, 2245, 2263, 2266, 2267, 2275, 2280, 2282, 2283,
2285, 2286, 2297, 2301, 2309, 2310, 2311, 2312, 2325, 2327,
2341, 2345, 2370, 2381, 2385, 2407, 2432, 2436, 2438, 2461,
2497, 2503, 2506, 2525, 2535, 2551, 2554, 2557, 2562, 2595,
2616, 2617, 2626, 2628, 2633, 2636, 2638, 2662, 2664, 2668,
2674, 2681, 2701, 2710, 2717, 2734, 2736, 2741, 2746, 2747,
2749, 2761, 2780, 2789, 2792, 2816, 2843, 2844, 2857, 2882,
2895, 2901, 2927, 2946, 2978, 3003, 3005, 3006, 3026, 3028,
3065, 3066, 3098, 3099, 3107, 3108, 3133, 3140, 3151, 3168,
3190, 3216, 3217, 3220, 3224, 3226, 3230, 3231, 3232, 3234,
3238, 3240, 3247, 3251, 3256, 3270, 3272, 3275, 3285, 3294,
3297, 3301, 3319, 3320, 3336, 3363, 3370, 3371, 3372, 3379,
3386, 3389, 3391, 3404, 3408, 3414, 3416, 3421, 3437, 3441,
3444, 3445, 3460, 3464, 3470, 3471, 3494, 3516, 3522, 3529,
3534, 3535, 3538, 3541, 3544, 3558, 3560, 3584, 3601, 3609,
3612, 3613, 3620, 3621, 3625, 3628, 3629, 3641, 3652, 3658,
3664, 3666, 3674, 3686, 3691, 3703, 3707, 3743, 3756, 3761,
3781, 3786, 3790, 3803, 3806, 3819, 3837, 3838, 3844, 3856,
3863, 3869, 3878, 3881, 3882, 3888, 3895, 3924, 3933, 3934,
3939, 3950, 3953, 3960, 3970, 3973, 3977, 3979, 3985, 3995]
>>>
"""

from __future__ import print_function
from syntagrus_reader import SynTagRusCorpusReader as reader
from itertools import chain
from math import pow
from nltk.parse import DependencyGraph
from copy import deepcopy

def dependents(sent,head): # head: node address
    """ -> sorted list of dep addresses """
    return sorted(chain.from_iterable(sent.nodes[head]\
                                      ['deps'].values()))    

def is_dominated(g,n1,n2): # g: graph; n1,n2: node addresses
    """ if n1 is dominated by n2 (True/False) """
    if 'head' in g.nodes[n1]:
        head = g.nodes[n1]['head']
        if head==n2:
            return True
        if is_dominated(g,head,n2):
            return True
    return False

def get_root(g,r,n): # g: graph; r: range; n: node address
    """  -> root of a connected component """
    if 'head' in g.nodes[n]:
        if g.nodes[n]['head'] not in r:
            return n
        else:
            return get_root(g,r,g.nodes[n]['head'])
    return n
    
def get_range(g,h,d): # g: graph; h: head node; d: dependent node
    """ -> range of addresses between two nodes, inclusively """
    addresses = sorted(g.nodes.keys())
    h_index = addresses.index(h)
    d_index = addresses.index(d)
    sign = cmp(d_index,h_index)
    return addresses[h_index:d_index+sign:sign]

def is_nonprojective_edge(g,h,d):
    """ if the edge between h and d is nonprojective (True/False) """
    rang = get_range(g,h,d)
    roots = set()
    for i in rang[1:-1]:
        roots.add(get_root(g,rang[1:-1],i))    
    for i in roots:
        if not is_dominated(g,i,h):
            return True
    return False        

def is_nonprojective(sent,node_index):
    """ if sent is a nonprojective graph (True/False) """
    children = dependents(sent,node_index)
    if children!=list():
        for c in children:
            if is_nonprojective_edge(sent,node_index,c):
                return True
            if is_nonprojective(sent,c):
                return True
    return False
    

def modify_addresses(graph,k): # k: address coefficient
    """ address-> address*k """
    def update_node(node,k):
        for d in node['deps']:
            for i in range(len(node['deps'][d])):
                node['deps'][d][i] *= k
        if node['address']!=0:
            node['address'] *= k
            node['head'] *= k
    output = DependencyGraph()
    for n in graph.nodes:
        output.nodes[n*k] = deepcopy(graph.nodes[n])
    for n in output.nodes:
        update_node(output.nodes[n],k)
    return output

def insert_nulls(g,gg,h,k): # g,gg:graphs, h:head, k:coefficient
    """ insert null elements to make nonprojective graph projective """
    ds = dependents(g,h)    
    if ds!=list():
        for d in ds:
            if is_nonprojective_edge(g,h,d):
                co_index = d/k
                r = get_range(g,h,d)
                r.reverse()
                for i in r[1:-1]:
                    if not is_nonprojective_edge(g,h,i):
                        base_index = i - k*(cmp(i,h)+1)/2
                        address = base_index + co_index
                        gg.add_node({
                            'ctag': str(co_index),
                            'tag': g.nodes[d]['tag'],
                            'word': '*NP2P*-'+str(co_index),
                            'head': h,
                            'address': address,
                            'rel': g.nodes[d]['rel']
                            })
                        gg.add_arc(h,address)
                        break
            insert_nulls(g,gg,d,k)

def chose_head(g,h,d): # g: graph; h: head; d: dependent
    """
    -> chose the closest projective head
    (necessary condition: 'head' in g.nodes[h]['head'])
    """
    if is_nonprojective_edge(g,h,d):
        return chose_head(g,g.nodes[h]['head'],d)
    return h

def move_up_node(g,i,k):  # i: node address of null element, k: coefficient
    """ move up the node conindexed with this node """
    d = i%k*k #d: address of dependent node coindexed with i
    # co-index stored in 'ctag'
    g.nodes[d]['ctag'] = g.nodes[i]['ctag']
    h = g.nodes[d]['head'] # assumption: 'head' exists
    h_new = chose_head(g,h,d)
    g.nodes[d]['head'] = h_new
    rel = g.nodes[d]['rel']
    g.nodes[d]['rel'] = 'NP2P'
    g.add_arc(h_new,d)
    g.nodes[h]['deps'][rel].remove(d)

def path(g): #g: graph
    """
    -> specific sequence of all the nodes in g
    such that any dependent node comes before its head
    """
    marked = set()
    nodes = set(g.nodes)    
    output = list()
    def recursive(g):
        for i in nodes.copy():
            d = dependents(g,i)
            if (not d) or all(dd in marked for dd in d):
                output.append((i,g.nodes[i]['word']))
                marked.add(i)
                nodes.remove(i)
                if nodes==set([0]):
                    break
                recursive(g)
                break
    recursive(g)
    return output

def move_up(g,k): # g: graph; k: coefficient
    """ -> move up all nodes coindexed with null elements """
    for i,_ in path(g): #i: node address
        if (i%k)!=0:
            move_up_node(g,i,k)

def np2p(g,k): #g: graph; k; coefficient
    """ convert non-projective to projective graph """
    temp = modify_addresses(g,k)
    output = deepcopy(temp)
    insert_nulls(temp,output,0,k)
    output.root = output.nodes[output.nodes[0]['deps']\
                               ['ROOT'][0]]
    move_up(output,k)    
    return output

if __name__ == "__main__":
    #r = reader('./SynTagRus_edited', r'(?!\.).*\.tgt')
    r = reader('./SynTagRus_edited/2011', r'(?!\.).*\.tgt')
    #k = int(pow(10,len(str(max(len(s.nodes) for s in sents)))))
    k = 10000    
    sents = r.parsed_sents()
    p_sents = [s for s in sents if not is_nonprojective(s,0)]
    n_sents = [s for s in sents if is_nonprojective(s,0)]
    n2p_sents_temp = [np2p(g,k) for g in n_sents]
    n2p_sents = [g for g in n2p_sents_temp
                 if not is_nonprojective(g,0)]
    troubled_sents = [g for g in n2p_sents_temp
                       if is_nonprojective(g,0)] # further study needed
    print('Number of projective sents: ',len(p_sents))
    print('Number of non-projective sents: ',len(n_sents))
    indexes = [i for i in range(len(sents))
               if is_nonprojective(sents[i],0)]
    print('Indexes of these sentences: ',indexes)

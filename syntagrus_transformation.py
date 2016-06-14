#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SynTagRus Tree Transformation Module
alexluu@brandeis.edu
"""

from nltk.tree import Tree, ParentedTree
from copy import deepcopy
import re
from collections import defaultdict

i_pattern = re.compile(r'^\d+$')

def analyze_label(label):
    """ -> dict of syntactic and functional tags """
    output = dict()
    temp = label.split('-')
    output['syntactic'] = temp[0]
    output['functional'] = set(temp[1:])
    return output

def get_label_positions(t,order="preorder"):
    """
    order: "preorder"/"postprder"/"bothorder"/"leaves"
    """
    output = t.treepositions(order)
    leaves = t.treepositions('leaves')
    for p in leaves:
        output.remove(p)
    return output

############################################################

def change_label(t,f_tag,s_tag):
    """ change s_tag of all nodes having f_tag """
    # set of positions of all labels in tree
    l_pos = get_label_positions(t)
    for p in l_pos:
        l = t[p].label()
        f_tags = analyze_label(l)['functional']
        if f_tag in f_tags:
            t[p].set_label(s_tag+''.join(l.partition('-')[1:]))

############################################################

def find_first_wh_leaf(t):
    """ -> 1st WH leaf in a WH phrase t """
    leaves = t.treepositions('leaves')
    for i in range(len(leaves)):
        f_tags = analyze_label(t[leaves[i][:-1]].label())\
                 ['functional']
        if 'WH' in f_tags:
            return i

def find_highest_unary(t,p):  #p: treeposition
    """ -> highest unary node dominating p """
    output = p
    if len(p): # p!=tuple()
        for i in range(len(p)):
            if len(t[p[:-(i+1)]])>1:
                break
        if i>0:
            output = p[:-i]
    return output 

def find_wh_phrase(t):
    wh_index = find_first_wh_leaf(t)
    if isinstance(wh_index,int):
        if wh_index==0: # handle trees[1331]
            wh_pos = t.leaf_treeposition(0)[:-2]
        else:
            wh_pos = t.treeposition_spanning_leaves(0,wh_index+1)
        return find_highest_unary(t,wh_pos)
    return "No WH leaf!"
    

def wh_movement(t,pos):
    cpos = find_wh_phrase(t[pos])
    if cpos=="No WH leaf!":
        pass
    elif not cpos:
        pass
    else:    
        ctemp = deepcopy(t[pos][cpos])
        clabel = analyze_label(ctemp.label())
        fs = clabel['functional']
        if all(not i_pattern.match(f) for f in fs):
            index = '-' + ''.join(str(i) for i in pos) + \
                    '1' + ''.join(str(i) for i in cpos)
            label = clabel['syntactic'] + index
            t[pos][cpos] = Tree(t[pos][cpos].label(),
                                ['*T*'+index])
        else:
            label = ctemp.label()
            del t[pos][cpos]
        ctemp.set_label('WH' + label)
        temp = deepcopy(t[pos])
        label = temp.label().partition('-')
        t[pos] = Tree('SBAR'+label[1]+label[2],[
                ctemp,
                temp
                ])

############################################################

def get_relative_nodes(t,order='postorder'):
    output = list()
    nodes = get_label_positions(t,order)
    for n in nodes:
        f_tags = analyze_label(t[n].label())['functional']
        if 'RLT' in f_tags or 'SBO' in f_tags:
            output.append(n)
    return output

def get_relative_structures(t,order='postorder'):
    """ Ignore null elements """
    output = list()
    nodes = get_label_positions(t,order)
    for n in nodes:
        if t[n].height()>2: # t contains more than just leaves
            f_tags = analyze_label(t[n].label())['functional']
            if 'RLT' in f_tags or 'SBO' in f_tags:
                output.append(n)
    return output

def transform_relative_structures(t):
    rlt_structures = get_relative_structures(t)
    for n in rlt_structures:
        wh_movement(t,n)

############################################################

def c_command(node1, node2):    #node1, node2: tree positions
    return (node1[:-1]==node2[:len(node1[:-1])]
            and node1[-1]!=node2[len(node1[:-1])])

def merge_nodes(t,parent): #parent: tree position
    p_label =t[parent].label().partition('-')  
    if len(p_label)==3:
        for c in t[parent]:
            if isinstance(c,Tree):
                if p_label[0].startswith(analyze_label\
                   (c.label())['syntactic']):
                    c.set_label(c.label()+'-'+p_label[2])
    new_index = parent[-1]+len(t[parent])
    for c in t[parent][::-1]:
        t[parent[:-1]].insert(parent[-1],c)	
    del t[parent[:-1]][new_index]    

############################################################

def np2p_leaves(tree):
    return set([p for p in tree.treepositions('leaves')
                if tree[p].startswith('*NP2P*')])

def np2p_coindexed_node(tree,leaf): #leaf: tree position
    coindex = tree[leaf].partition('-')[2]
    for p in get_label_positions(tree):
        if coindex in analyze_label(tree[p].label())\
           ['functional']:
            return p

def np2p_root(node,leaf):   #node, leaf: tree positions
    for i in range(len(node)):
        if i==len(leaf) or node[i]!=leaf[i]:
            break
    return node[:i]

def get_np2p_roots(t,order='postorder'):    # only problematic ones
    np2p_roots = defaultdict(list)
    for l in np2p_leaves(t):
        n = np2p_coindexed_node(t,l)
        if not c_command(n,l):
            np2p_roots[np2p_root(n,l)].append((t[n].label(),
                                               t[l]))
    nodes = get_label_positions(t,order)
    return [n for n in nodes if n in np2p_roots],np2p_roots

def order_labels(tree,labels,order='preorder'): #labels: list of labels of coindexed nodes
    np2p_coindexed_nodes = dict()
    for p in get_label_positions(tree):
        if tree[p].label() in labels:
            np2p_coindexed_nodes[p] = tree[p].label()            
    nodes = get_label_positions(tree,order)
    ordered = [n for n in nodes if n in np2p_coindexed_nodes]
    return [np2p_coindexed_nodes[p] for p in ordered]


def transform_np2p_structures(t): #to satisfy c-command condition
    ordered, targets = get_np2p_roots(t)
    for p in ordered:
        tree = t[p]
        labels = [x[0] for x in targets[p]]
        ordered_labels = order_labels(tree,labels)
        for l in labels:
            for pp in get_label_positions(tree):
                if tree[pp].label()==l:
                    break
            for i in range(len(pp)-1):
                merge_nodes(tree,pp[:-(i+1)])

############################################################

def transform_coordinative_structures(tree):
    flag = False
    nodes = get_label_positions(tree,order='postorder')
    for n in nodes[:-1]:
        s_tag = analyze_label(tree[n].label())['syntactic']
        f_tags = analyze_label(tree[n].label())['functional']
        pf_tags = set()
        if len(n):  #if n has parent
            ps_tag = analyze_label(tree[n[:-1]].label())\
                      ['syntactic']
            pf_tags = analyze_label(tree[n[:-1]].label())\
                      ['functional']
        if ('CRC' in f_tags)or \
           (('CRD' in f_tags) and ('CRD' in pf_tags) and
            s_tag == ps_tag) or \
           (('SCR' in f_tags) and ('SCR' in pf_tags) and
            s_tag == ps_tag):
            merge_nodes(tree,n)
            flag = True
            break
    if flag:
        transform_coordinative_structures(tree)
    return flag

if __name__ == "__main__":
    pass

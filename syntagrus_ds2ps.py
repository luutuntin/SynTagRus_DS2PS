#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SynTagRus DS2PS Module
alexluu@brandeis.edu

Demo:
>>> 
DS to DS+
Total conversion time: 62.7150001526 s

DS+ to PS+
Total conversion time: 111.552999973 s

Number of sentences: 49421
Number of p-sentences: 44421
Number of n-sentences: 5000
Number of n2p-sentences: 4994
Number of p-trees: 44421
Number of n2p-trees: 4994
>>>
"""

from __future__ import print_function
from syntagrus_reader import SynTagRusCorpusReader as reader
from collections import defaultdict
from itertools import chain
from syntagrus_grammar import *
from syntagrus_projectivity import np2p,is_nonprojective
import random
import time
from syntagrus_utils import save_data
from nltk.tree import Tree
from nltk.parse import DependencyGraph
from syntagrus_lemmas import get_lemmas

lemma_lists = 'syntagrus_lemma-lists.xml'
lemma_reader = reader('./',lemma_lists)
#wh_lemmas = get_lemmas(lemma_reader.xml(lemma_lists)[0])
wh_lemmas = [l for l in get_lemmas(lemma_reader.xml(lemma_lists)[0])]

def head_deps(graph,head,flag): # head: node, flag: 'C'/'A'
    """
    -> head's projection chain (flag=='C') OR
       attachment positions of head's dependents
                            in head's projection chain (flag=='A')
    """
    deps = [get_projection(head,graph.nodes[v],d,'H')
            for d in head['deps'] for v in head['deps'][d]]
    
    if flag=='C': # projection chain
        f_tag = str()
        if head['rel']!='ROOT': # and, of course, !='TOP'
            p_chains = [get_projection\
                        (graph.nodes[head['head']],\
                         head,head['rel'],'D')['p_chain']]
            if p_chains[0]:
                if len(p_chains[0][0])==3:
                    f_tag = p_chains[0][0][2]
        else:
            p_chains = list()

        p_chains.extend(d['p_chain'] for d in deps)
        labels = ['SS',x2xp(head)]
        l_num = defaultdict(int)
        for l in labels:
            temp = [ll[1] for c in p_chains for ll in c                    
                          if ll[0]==l]
                        
            if temp: # if this label exists
                l_num[l]=max(temp)
        return ([(l,l_num[l])
                for l in labels if l_num[l]],f_tag)
    
    elif flag=='A': # attachment positions
        attachments = dict()
        for d in deps:
            attachments[d['d_address']] = dict()
            attachments[d['d_address']]['label'] = \
            d['p_chain'][d['a_level']][0]
            attachments[d['d_address']]['offset'] = \
            d['offset']
            if 'f_tag' in d:
                attachments[d['d_address']]['f_tag'] = \
                d['f_tag']
        return attachments
            
    return "Invalid flag!"
        
def build_tree(node,chain): # -> handle function tags
    """ -> PS tree of node's projection chain """
    preterminal = node['tag']
    if 'lemma' in node: # not a trace-node
        if (node['lemma'].lower() in wh_lemmas) and \
           node['tag']!='CONJ': #WH feature
            preterminal += '-WH'    
    output = Tree(preterminal,[node['word']])
    for l in chain[0][::-1]:
        for i in range(l[1]):
            output = Tree(l[0],[output])
    if chain[1]:
        if chain[1]=='PRN':
            output = Tree(chain[1],[output])
        else:
            output.set_label(output.label()+'-'+chain[1])
    return output

def build_trees(graph):
    """ -> PS trees for projection chain of all nodes in graph """
    for n in graph.nodes:   # n: key index
        if n!=0:
            chain = head_deps(graph,graph.nodes[n],flag='C')
            yield (n,chain,build_tree(graph.nodes[n],chain))

def attach_tree(head,dep,attachment,chain,indexes,flag,coindex=None):
    #head,dep: trees; flag: 'right'/'left'
    """ attach dep's projection chain to head's projection chain """
    if isinstance(coindex,int): # handle coindex tag
        label = attachment['label2']
        offset = attachment['offset2']
        dep = Tree(dep.label(),['*-'+str(coindex)])        
    else:
        label = attachment['label']
        offset = attachment['offset']
        
    l_index = [l[0] for l in chain[0]].index(label)
    count = sum([l[1] for l in chain[0]][:l_index+1])-offset
    if flag=='right':
        a_index = indexes[count-1]+1
    elif flag=='left':
        a_index = indexes[count-1]
        indexes[count-1] += 1
    else:
        return "Invalid flag!"
    if head.label()=='PRN':
        s = 'head[0]'
    else:
        s = 'head'
    for i in range(count-1):
        s += '['+str(indexes[i])+']'
    eval(s+'.insert('+str(a_index)+',dep)') # insert() vs pop()
    
    if 'f_tag' in attachment:
        if attachment['f_tag'] not in {'PRD','PRDs'}:
            eval(s+'.set_label('+s+'.label()+"-"+attachment["f_tag"])')
        else:
            s += '['+str(indexes[count-1])+']'
            eval(s+'.set_label('+s+'.label()+"-"+attachment["f_tag"])')
    return head,indexes

def attach_trees(graph,head,trees): # head: address
    """
    -> PS tree of head's unit graph
    (if d<h: left to right; if h<d: right to left)
    """
    output = trees[head]['tree']
    indexes = [0]*(output.height()-2)
    attachments = head_deps(graph,graph.nodes[head],flag='A')
    d_addresses = sorted(attachments.keys()) # dep addresses
    left = [i for i in d_addresses if i<head]
    right = d_addresses[len(left):]

    def add_attachment(a1,a2):
        if (a1['label']==a2['label'] and
            a1['offset']<a2['offset']) or \
           (a1['label']!='SS' and a2['label']=='SS'):
            a1['label2'] = a1['label']  #trace
            a1['label'] = a2 ['label']
            a1['offset2'] = a1['offset']#trace
            a1['offset'] = a2['offset']
            return True
        return False

    # i is closer to the head than j
    for i in range(len(left)-2,-1,-1):
        for j in range(i+1,len(left)):            
            if add_attachment(attachments[left[i]],
                              attachments[left[j]]):
                break
                
    for i in range(1,len(right)):
        for j in range(i-1,-1,-1):
            if add_attachment(attachments[right[i]],
                              attachments[right[j]]):
                break

    for i in left:
        if 'label2' in attachments[i]:
            output,indexes = attach_tree(output,
                             trees[i]['tree'],
                             attachments[i],
                             trees[head]['chain'],
                             indexes,'left',i)
            trees[i]['tree'].set_label(trees[i]['tree'].\
                             label() + '-' + str(i))
        output,indexes = attach_tree(output,
                         trees[i]['tree'],
                         attachments[i],
                         trees[head]['chain'],
                         indexes,'left')                    
    
    for i in right[::-1]:
        if 'label2' in attachments[i]:
            output,indexes = attach_tree(output,
                             trees[i]['tree'],
                             attachments[i],
                             trees[head]['chain'],
                             indexes,'right',i)
            trees[i]['tree'].set_label(trees[i]['tree'].\
                             label() + '-' + str(i))
        output,indexes = attach_tree(output,
                         trees[i]['tree'],
                         attachments[i],
                         trees[head]['chain'],
                         indexes,'right')        
    return output

def deps(sent,head): # head: address
    """ -> dependents of head """    
    return sorted(chain.from_iterable(sent.nodes[head]\
                                      ['deps'].values()))

def path(graph):
    """
    -> specific sequence of all the nodes in g
    such that any dependent node comes before its head
    """
    marked = set()
    nodes = set(graph.nodes)
    output = list()
    def recursive(graph):
        for n in nodes.copy():
            d = deps(graph,n)
            if (not d) or all(dd in marked for dd in d):
                output.append((n,graph.nodes[n]['word']))
                marked.add(n)
                nodes.remove(n)
                if nodes==set([0]):
                    break
                recursive(graph)
                break
    recursive(graph)				  
    return output
    
def ds2ps(graph):
    """ -> convert projective DS+ graph to preliminary PS+ tree """
    trees = defaultdict(dict)
    for (n,c,t) in build_trees(graph):
        trees[n]['chain'] = c
        trees[n]['tree'] = t        
    if len(trees)>1:
        p = path(graph)
        for n in p:
            trees[n[0]]['tree'] = attach_trees(graph,n[0],trees)
        o_index = p[-1][0]
    else:
        o_index = 1
    return trees[o_index]['tree']

def test_word_order(graphs,trees):
    """ if converted PS+ trees preserve original word order """
    if len(graphs)==len(trees):
        #pass
        output = list() # unhappy cases
        for i in range(len(graphs)):
            g_words = [graphs[i].nodes[j]['word']
                       for j in sorted(graphs[i].nodes.keys())[1:]
                       if 'word' in graphs[i].nodes[j]
                       if not graphs[i].nodes[j]['word'].\
                       startswith('*')]
            t_words = [l for l in trees[i].leaves()
                       if not l.startswith('*')]
            if g_words!=t_words:
                print(i)
                print(' '.join(g_words))
                print(' '.join(t_words))
                output.append(i)
        return output
    return "Invalid inputs!"

if __name__ == "__main__":
    print("DS to DS+")
    t0 = time.time()
    r = reader('./SynTagRus_edited', r'(?!\.).*\.tgt')
    #r = reader('./SynTagRus_edited/2011', r'(?!\.).*\.tgt')
    sents = r.parsed_sents()
    p_sents = [s for s in sents if not is_nonprojective(s,0)]
    n_sents = [s for s in sents if is_nonprojective(s,0)]
    #n = 1000
    n = 10000
    n2p_sents_temp = [np2p(g,n) for g in n_sents]
    n2p_sents = [g for g in n2p_sents_temp
                 if not is_nonprojective(g,0)]
    print('Total conversion time:',time.time()-t0,'s')
    print("\nDS+ to PS+")
    t0 = time.time()
    p_trees = [ds2ps(g) for g in p_sents]    
    n2p_trees_temp = [ds2ps(g) for g in n2p_sents_temp]
    n2p_trees = [n2p_trees_temp[i] for i in range(len(n2p_trees_temp))
                 if not is_nonprojective(n2p_sents_temp[i],0)]
    print('Total conversion time:',time.time()-t0,'s')
    p_test = test_word_order(p_sents,p_trees)
    n2p_test = test_word_order(n2p_sents,n2p_trees)
    print("\nNumber of sentences:",len(sents))
    print("Number of p-sentences:",len(p_sents))
    print("Number of n-sentences:",len(n_sents))
    print("Number of n2p-sentences:",len(n2p_sents))
    print("Number of p-trees:",len(p_trees)-len(p_test))
    print("Number of n2p-trees:",len(n2p_trees)-len(n2p_test))
    p_graphs = [g.tree() for g in p_sents]
    n_graphs = [g.tree() for g in n_sents]
    #n2p_graphs = [g.tree() for g in n2p_sents]
    n2p_graphs_temp = [g.tree() for g in n2p_sents_temp]
##    save_data(p_graphs,'p_graphs.pkl')
##    save_data(n_graphs,'n_graphs.pkl')
##    save_data(n2p_graphs_temp,'n2p_graphs_temp.pkl')    
##    save_data(p_trees,'p_trees.pkl')
##    save_data(n2p_trees_temp,'n2p_trees_temp.pkl')

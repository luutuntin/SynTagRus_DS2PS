#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SynTagRus Annotation Information Module
alexluu@brandeis.edu

Demo:
>>> 
auxiliary
аналит пасс-анал вспом колич-вспом соотнос эксплет пролепт 

attributive_modificative
опред оп-опред релят 

attributive_quantitative
количест аппрокс-колич колич-копред колич-огран распред аддит 

coordinative
сочин сент-соч соч-союзн кратн 

attributive_appositive
аппоз об-аппоз ном-аппоз нум-аппоз 

actant
предик дат-субъект агент квазиагент несобст-агент 1-компл 2-компл 3-компл 4-компл 5-компл присвяз 1-несобст-компл 2-несобст-компл 3-несобст-компл 4-несобст-компл неакт-компл компл-аппоз предл подч-союзн инф-союзн сравнит сравн-союзн электив сент-предик адр-присв 

attributive_adverbial
обст длительн кратно-длительн дистанц обст-тавт суб-обст об-обст суб-копр об-копр огранич вводн изъясн разъяснит примыкат уточн 

attributive_attributive
атриб композ 

>>> 
"""

from __future__ import print_function
from syntagrus_reader import SynTagRusCorpusReader as reader

def get_rels(abs_group):
    """ """
    return [c.get('name') for c in list(abs_group)]

def rel_dict(rel_annotation):
    """ """
    rels = dict()
    for g in list(rel_annotation): # rel group
        if g.findall('subgroup')!=list():
            for sg in list(g): # rel subgroup
                rels[g.get('name')+'_'+sg.get('name')] = \
                get_rels(sg)
        else:
            rels[g.get('name')] = get_rels(g)
    return rels
    
if __name__ == "__main__":
    #tagsets = 'syntagrus_tagsets.xml'
    tagsets = 'syntagrus_tagsets_2011.xml'
    r = reader('./',tagsets)
    rel_annotation = r.xml(r.fileids()[0])[1]
    rels = rel_dict(rel_annotation)
    for k in rels:
        print(k)
        for v in rels[k]:
            print(v,end=' ')
        print('\n')

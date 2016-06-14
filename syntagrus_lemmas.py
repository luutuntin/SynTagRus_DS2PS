#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SynTagRus Special Lemmas Module
alexluu@brandeis.edu

Demo:
>>> 
который
кто
что
какой
как
где
куда
когда
почему
зачем
>>> 
"""

from syntagrus_reader import SynTagRusCorpusReader as reader

def get_lemmas(lemma_list):
    """ """
    for lemma in list(lemma_list):
        yield lemma.get('form')
    
if __name__ == "__main__":
    lemma_lists = 'syntagrus_lemma-lists.xml'
    r = reader('./',lemma_lists)
    wh_lemmas = get_lemmas(r.xml(lemma_lists)[0])
    for lemma in wh_lemmas:
        print(lemma)

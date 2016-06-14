# -*- coding: utf-8 -*-

"""
SynTagRus PS TreeBank Module
alexluu@brandeis.edu

Demo:
>>>
...
>>>
"""
from __future__ import print_function
from syntagrus_reader import SynTagRusCorpusReader as reader
from syntagrus_projectivity import np2p,is_nonprojective
from syntagrus_ds2ps import ds2ps
from syntagrus_transformation import *
from syntagrus_utils import load_data,save_data,write_lines
import os
import shutil
import time
from copy import deepcopy

def ds2ps_for_file(ds_treebank,base_path,fileid):
    """ """
    ps_file = '.'.join([fileid.partition('.')[0],'mrg'])
    sents = ds_treebank.parsed_sents([fileid])
    lines = list()
    for sent in sents:
        if is_nonprojective(sent,0):
            temp = np2p(sent,10000)
        else:
            temp = sent
        if is_nonprojective(temp,0):
            lines.append("We are sorry that the conversion of this sentence is not available now.")
        else:
            tree = ds2ps(temp)
            change_label(tree,'SBD','SBAR')
            transform_relative_structures(tree)
            transform_np2p_structures(tree)
            transform_coordinative_structures(tree)
            lines.append(tree.pformat()+'\n\n')
    write_lines(lines,os.path.join(base_path,ps_file))

def create_ps_treebank(ds_treebank,
                       base_path=os.getcwd(),
                       dir_name='ps_treebank'): #ds_treebank: SynTagRus reader 
    """ """
    ps_treebank_path = os.path.join(base_path,dir_name)
    if os.path.exists(ps_treebank_path):
        shutil.rmtree(ps_treebank_path)
    os.makedirs(ps_treebank_path)
    subdirs = ds_treebank.subdirs()
    for subdir in ds_treebank.subdirs():
        if subdir!='':
            os.mkdir(os.path.join(ps_treebank_path,subdir))        
    for fileid in ds_treebank.fileids():
        ds2ps_for_file(ds_treebank,ps_treebank_path,fileid)
        
if __name__ == "__main__":    
    t0 = time.time()    
    r = reader('./SynTagRus_edited', r'(?!\.).*\.tgt')
    #r = reader('./SynTagRus_edited/2011', r'(?!\.).*\.tgt')
    create_ps_treebank(r)
    #create_ps_treebank(r,dir_name='2011')
    print('Total conversion time:',time.time()-t0,'s')

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SynTagRus File Utils Module
alexluu@brandeis.edu

Reference:
https://github.com/luutuntin/Cinderella/blob/master/semaland_utils.py
"""
from cPickle import dump, load, HIGHEST_PROTOCOL
import codecs

def read_lines(data_file):
    """ data file -> lines (strings) """
    with codecs.open(data_file,'r',encoding='utf-8') as f:
        for line in f.readlines():
            yield line

def write_lines(lines,data_file):
    """ lines -> data file """
    with codecs.open(data_file,'w',encoding='utf-8') as f:
        for line in lines:
            f.write(line)

def save_data(data,pklfile_name):
    """ save data to a pickle file """        
    with open(pklfile_name,'wb') as f:
        dump(data,f,HIGHEST_PROTOCOL)

def load_data(pklfile_name):
    """ load data from a pickle file """        
    with open(pklfile_name,'rb') as f:
        return load(f)

if __name__ == "__main__":
    pass

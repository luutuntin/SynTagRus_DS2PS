#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SynTagRus Corpus Reader Module
alexluu@brandeis.edu

Demo:
>>> ================================ RESTART ================================
>>> 
Please enter your corpus path (example: ./SynTagRus):
./SynTagRus
>>> type(r)
<class '__main__.SynTagRusCorpusReader'>
>>> r.subdirs()
['2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', 'news', 'uppsala']
>>> files = r.fileids(subdir = '2004')
>>> files
['2004/Andrei_Ashkerov.tgt', '2004/Tarifnaya_viselitsa.tgt']
>>> annotated_words = r.annotated_words(files)
>>> len(annotated_words)
2628
>>> w = annotated_words[1]
>>> type(w)
<type 'Element'>
>>> print(w.text)
января
>>> for i in w.attrib.items():
	print(i[0] + ': ' + i[1])

	
LEMMA: ЯНВАРЬ
FEAT: S ЕД МУЖ РОД НЕОД
ID: 2
LINK: атриб
DOM: 1
>>> annotated_sents = r.annotated_sents(files)
>>> len(annotated_sents)
139
>>> s = annotated_sents[0]
>>> type(s)
<type 'Element'>
>>> w = s[1]
>>> type(w)
<type 'Element'>
>>> print(w.text)
января
>>> print(w.text)
января
>>> for i in w.attrib.items():
	print(i[0] + ': ' + i[1])

	
LEMMA: ЯНВАРЬ
FEAT: S ЕД МУЖ РОД НЕОД
ID: 2
LINK: атриб
DOM: 1
>>> parsed_sents = r.parsed_sents(files)
>>> len(parsed_sents)
139
>>> s = parsed_sents[0]
>>> t = s.tree()
>>> t.pprint()
(стало (23 (января (года 2002))) не (Пьера Бурдье))
>>>
"""

from __future__ import print_function
from nltk.corpus.reader.xmldocs import XMLCorpusReader
import os
from os.path import dirname, join, isdir
import codecs
from nltk.parse import DependencyGraph
from nltk import compat
from nltk.corpus.reader.util import concat

class SynTagRusCorpusReader(XMLCorpusReader):
    """ inherit 'xml(fileid)' and 'words(fileid)' """
    def __init__(self, root, fileids):
        """ """
        super(SynTagRusCorpusReader, self).\
              __init__(root, fileids)

    def subdirs(self):
        """ -> list of subdirectories in the corpus """
        return sorted(set(dirname(f) for f in super\
               (SynTagRusCorpusReader,self).fileids()))

    def fileids(self, subdir=None):
        """ -> list of files in a corpus subdirectory """
        if subdir is None:
            return super(SynTagRusCorpusReader,self).\
                         fileids()
        elif isdir(join(self.root,subdir)):
            return [f for f in super(SynTagRusCorpusReader,\
                    self).fileids() if subdir in f]
        else:
            raise ValueError('Subdirectory %r is invalid.'
                             % subdir)

    def raw(self, fileids=None):
        """ re-define method 'raw()' of XMLCorpusReader """
        if fileids is None:
            fileids = self._fileids
        elif isinstance(fileids, compat.string_types):
            fileids = [fileids]
        return concat([codecs.open(f, encoding =
               'windows-1251').read() for f in fileids])

    def annotated_words(self, fileids=None):
        """ -> list of annotated words in fileids """
        return [w for f in self.abspaths(fileids)
                  for w in self.xml(f).findall('./body/S/W')]

    def annotated_sents(self, fileids=None):
        """ -> list of annotated sents in fileids """
        return [s for f in self.abspaths(fileids)
                  for s in self.xml(f).findall('./body/S')]    

    def parsed_sents(self, fileids=None):
        """ -> list of parsed sents in fileids """

        def normalize(string):
            """ replace whitespaces/empty string by underscore(s) """
            if string:
                return string.replace(' ', '_')
            return '_'

        def word2conll2007(word):
            """ -> conll2007 format of an annotated word """            
            if word.get('FEAT'):
                tag, _, feats = word.get('FEAT').partition(' ')
            else:
                tag = 'UNK' #'2010/Nadpisi_iz_doliny_Inda.tgt'-38-13
                feats = None            
            head = word.get('DOM')
            rel = word.get('LINK')            
            if head == '_root':
                head = '0'                
                rel = 'ROOT'            
            output=' '.join([
                             word.get('ID'),
                             normalize(word.text),
                             normalize(word.get('LEMMA')),
                             tag,
                             tag,
                             normalize(feats),
                             head,
                             rel,
                             head,
                             rel
                            ])
            return output
        def sent2conll2007(sent):
            """ -> conll2007 format of an annotated sent """
            return [word2conll2007(w) for w in list(sent)]
        
        return [DependencyGraph(sent2conll2007(sent))
                for sent in self.annotated_sents(fileids)]
    
if __name__ == "__main__":
    def get_corpus_path():
        """ """
        corpus_path = raw_input\
                      ("Please enter your corpus path " +
                       "(example: ./SynTagRus):\n")
        if os.access(corpus_path,os.F_OK):
            return corpus_path
        else:
            print('This path does not exist.\n')
            return get_corpus_path()
    r = SynTagRusCorpusReader(get_corpus_path(),
                              r'(?!\.).*\.tgt')

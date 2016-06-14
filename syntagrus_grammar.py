#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SynTagRus Grammar Heuristics Module
alexluu@brandeis.edu

Demo:
"""
from __future__ import print_function
from syntagrus_reader import SynTagRusCorpusReader as reader
from syntagrus_info import rel_dict

X2XP = {
        'S':    'NP',
        'A':    'ADJP',
        'V':    'VP',
        'ADV':  'ADVP',
        'NUM':  'QP',
        'PR':   'PP',
        'CONJ': 'CONJP',
        'PART': 'PRT',
        'P':    'INTJ',
        'INTJ': 'INTJ', #<-> UH in Penn Treebank POS tags
        'NID':  'NP',        
        }   #'COM' -> modifier in NP

def x2xp(node): #type(node): dict
    """ -> phrase-level label (str) """
    if node['tag'] in X2XP:
        return X2XP[node['tag']]
    else:
        return 'XP'

tagsets = 'syntagrus_tagsets_2011.xml'
r = reader('./',tagsets)
rel_annotation = r.xml(r.fileids()[0])[1]
rels = rel_dict(rel_annotation)


def get_projection(head,dep,rel,flag): #head, dep: nodes
    """ -> dict{'p_chain'[,'d_address','a_level','offset','f_tag']} """
    output = dict()
    p_chain = list()    #projection chain

    if flag=='H':
        a_level = int() #attachment level of dep phrase
        offset = int()  #how high a_level is
        f_tag = str()   #function tag related to attachment
        xp = x2xp(head)

        if rel==rels['actant'][0]:                  #*predicative
            p_chain = [('SS',1),(xp,1)]
            a_level = 0
            offset = 0
            if xp!='VP':
                f_tag = 'PRD'
        if rel==rels['actant'][1]:                  #dative-subjective
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['actant'][2]:                  #agentive
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['actant'][3]:                  #quasiagentive
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['actant'][4]:                  #improper agentive
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel in rels['actant'][5:10]:             #completive
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['actant'][10]:                 #copulative
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            f_tag = 'CPL'
        if rel in rels['actant'][11:15]:            #improper completive
            p_chain = [('SS',1),(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['actant'][15]:                 #nonactant-completive
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['actant'][16]:                 #completive-appositive
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['actant'][17]:                 #prepositional
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['actant'][18]:                 #subordinative-conjunctive
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            f_tag = 'SBD'
        if rel==rels['actant'][19]:                 #infinitive-conjunctive
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            f_tag = 'SBD'
        if rel==rels['actant'][20]:                 #comparative
            p_chain = [(xp,2)]
            a_level = 0
            offset = 1
            f_tag = 'CPR'
        if rel==rels['actant'][21]:                 #comparative-conjunctive
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            f_tag = 'CPC'
        if rel==rels['actant'][22]:                 #elective
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['actant'][23]:                 #*sentential-predicative
            p_chain = [('SS',2),(xp,1)]
            a_level = 0
            offset = 1
            f_tag = 'PRDs'
        if rel==rels['actant'][24]:                 #addressee-copulative
            p_chain = [(xp,2)]
            a_level = 0
            offset = 1
            #f_tag = ''

        if rel==rels['attributive_modificative'][0]:#proper modificative
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_modificative'][1]:#descriptive-modificative
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_modificative'][2]:#relative
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
            
        if rel==rels['attributive_attributive'][0]: #proper attributive
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_attributive'][1]: #composite
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            f_tag = 'CPS'
            
        if rel==rels['attributive_appositive'][0]:  #proper appositive
            p_chain = [(xp,2)]
            a_level = 0
            offset = 1
            #f_tag = ''
        if rel==rels['attributive_appositive'][1]:  #separate appositive
            p_chain = [(xp,2)]
            a_level = 0
            offset = 1
            #f_tag = ''
        if rel==rels['attributive_appositive'][2]:  #nominative-appositive
            p_chain = [(xp,2)]
            a_level = 0
            offset = 1
            #f_tag = ''
        if rel==rels['attributive_appositive'][3]:  #numerative-appositive
            p_chain = [(xp,2)]
            a_level = 0
            offset = 1
            #f_tag = ''
            
        if rel==rels['attributive_quantitative'][0]:#proper quantitative
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_quantitative'][1]:#approximative-quantitative
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_quantitative'][2]:#quantitative-copredicative
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_quantitative'][3]:#quantitative-restrictive
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_quantitative'][4]:#distributive
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_quantitative'][5]:#additive
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''

        if rel==rels['attributive_adverbial'][0]:   #proper adverbial/circumstantial
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_adverbial'][1]:   #durative
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_adverbial'][2]:   #multiple durative
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_adverbial'][3]:   #distant
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_adverbial'][4]:   #adverbial-tautological
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_adverbial'][5]:   #subective-adverbial
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_adverbial'][6]:   #objective-adverbial
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_adverbial'][7]:   #subjective-copredicative
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_adverbial'][8]:   #objective-copredicative
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['attributive_adverbial'][9]:   #restrictive
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            f_tag = 'RES'
        if rel==rels['attributive_adverbial'][10]:  #parenthetic(al)
            p_chain = [(xp,2)]
            a_level = 0
            offset = 1
            #f_tag = ''
        if rel==rels['attributive_adverbial'][11]:  #subordinative
            p_chain = [(xp,2)]
            a_level = 0
            offset = 1
            #f_tag = ''
        if rel==rels['attributive_adverbial'][12]:  #explanatory
            p_chain = [(xp,2)]
            a_level = 0
            offset = 1
            #f_tag = ''
        if rel==rels['attributive_adverbial'][13]:  #adjoining
            p_chain = [(xp,2)]
            a_level = 0
            offset = 1
            #f_tag = ''
        if rel==rels['attributive_adverbial'][14]:  #specifying
            p_chain = [(xp,2)]
            a_level = 0
            offset = 1
            #f_tag = ''

        if rel==rels['coordinative'][0]:            #coordinative
            p_chain = [(xp,2)]
            a_level = 0
            offset = 1
            f_tag = 'CRD'
        if rel==rels['coordinative'][1]:            #sentential-coordinative
            p_chain = [('SS',2),(xp,1)]
            a_level = 0
            offset = 1
            f_tag = 'SCR'
        if rel==rels['coordinative'][2]:            #coordinative-conjunction
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            f_tag = 'CRC'
        if rel==rels['coordinative'][3]:            #multiple
            #p_chain = [(xp,2)]
            p_chain = [(xp,1)]
            a_level = 0
            #offset = 1
            offset = 0
            f_tag = 'MTP'

        if rel==rels['auxiliary'][0]:               #analytical
            #p_chain = [(xp,2)]
            p_chain = [(xp,1)]
            a_level = 0
            #offset = 1
            offset = 0
            f_tag = 'ANL'
        if rel==rels['auxiliary'][1]:               #passive-analytical
            #p_chain = [(xp,2)]
            p_chain = [(xp,1)]
            a_level = 0
            #offset = 1
            offset = 0
            f_tag = 'PAN'
        if rel==rels['auxiliary'][2]:               #auxiliary
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            f_tag = 'AXL'
        if rel==rels['auxiliary'][3]:               #quantitative-auxiliary
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''
        if rel==rels['auxiliary'][4]:               #correlative
            p_chain = [(xp,2)]
            a_level = 0
            offset = 1
            f_tag = 'CRL'
        if rel==rels['auxiliary'][5]:               #expletive
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = 'EXP'
        if rel==rels['auxiliary'][6]:               #proleptic
            #p_chain = [('SBAR',1),('S',1),(xp,1)]
            p_chain = [(xp,1)]
            a_level = 0
            offset = 0
            #f_tag = ''

        if rel=='NP2P':
            p_chain = [(xp,2)]
            a_level = 0
            offset = 1
            f_tag = rel
            
        output['d_address'] = dep['address']
        output['a_level'] = a_level
        output['offset'] = offset
        if f_tag:
            output['f_tag'] = f_tag

    elif flag=='D':
        xp = x2xp(dep)
        if rel==rels['actant'][0]:                  #predicative
            p_chain = [(xp,1,'SBJ')]
        if rel==rels['actant'][1]:                  #dative-subjective
            p_chain = [(xp,1,'DTS')]
        if rel==rels['actant'][2]:                  #agentive
            p_chain = [(xp,1,'LGS')]
        if rel==rels['actant'][3]:                  #quasiagentive
            p_chain = [(xp,1,'LGSq')]
        if rel==rels['actant'][4]:                  #improper agentive
            p_chain = [(xp,1,'LGSi')]
        if rel in rels['actant'][5:10]:             #completive
            p_chain = [(xp,1)]
        if rel==rels['actant'][10]:                 #copulative
            p_chain = [(xp,1,'PRD')]
        if rel in rels['actant'][11:15]:            #improper completive
            p_chain = [(xp,1,'TPC')]
        if rel==rels['actant'][15]:                 #nonactant-completive
            p_chain = [(xp,1,'NAT')]
        if rel==rels['actant'][16]:                 #completive-appositive
            p_chain = [(xp,1,'CAP')]
        if rel==rels['actant'][17]:                 #prepositional
            p_chain = [(xp,1)]
        if rel==rels['actant'][18]:                 #subordinative-conjunctive
            p_chain = [('SS',1),(xp,1)]
        if rel==rels['actant'][19]:                 #infinitive-conjunctive
            p_chain = [('SS',1,'INF'),(xp,1)]
        if rel==rels['actant'][20]:                 #comparative
            p_chain = [(xp,1)]
        if rel==rels['actant'][21]:                 #comparative-conjunctive
            p_chain = [(xp,1)]
        if rel==rels['actant'][22]:                 #elective
            p_chain = [(xp,1,'ELT')]
        if rel==rels['actant'][23]:                 #sentential-predicative
            p_chain = [(xp,1,'SBJ')]
        if rel==rels['actant'][24]:                 #addressee-copulative
            p_chain = [(xp,1,'ACP')]

        if rel==rels['attributive_modificative'][0]:#proper modificative
            p_chain = [('',0,'MDF')]
        if rel==rels['attributive_modificative'][1]:#descriptive-modificative
            p_chain = [('',0,'DSC')]
        if rel==rels['attributive_modificative'][2]:#relative
            p_chain = [('',0,'RLT')]
            
        if rel==rels['attributive_attributive'][0]: #proper attributive
            p_chain = [(xp,1,'ATB')]
        if rel==rels['attributive_attributive'][1]: #composite
            p_chain = []
            
        if rel==rels['attributive_appositive'][0]:  #proper appositive
            p_chain = [(xp,1,'APS')]
        if rel==rels['attributive_appositive'][1]:  #separate appositive
            p_chain = [(xp,1,'SAP')]
        if rel==rels['attributive_appositive'][2]:  #nominative-appositive
            p_chain = [(xp,1,'NOA')]
        if rel==rels['attributive_appositive'][3]:  #numerative-appositive
            p_chain = [(xp,1,'NUA')]
            
        if rel==rels['attributive_quantitative'][0]:#proper quantitative
            p_chain = [('',0,'QTT')]
        if rel==rels['attributive_quantitative'][1]:#approximative-quantitative
            p_chain = [('',0,'APQ')]
        if rel==rels['attributive_quantitative'][2]:#quantitative-copredicative
            p_chain = [(xp,1,'QCP')]
        if rel==rels['attributive_quantitative'][3]:#quantitative-restrictive
            p_chain = [('',0,'QRS')]
        if rel==rels['attributive_quantitative'][4]:#distributive
            p_chain = [(xp,1,'DST')]
        if rel==rels['attributive_quantitative'][5]:#additive
            p_chain = [(xp,1,'ADT')]

        if rel==rels['attributive_adverbial'][0]:   #proper adverbial/circumstantial
            #if xp!='ADVP' or xp!='PP':
            if xp!='ADVP' and xp!='PP':
                p_chain = [(xp,1,'ADV')]
            else:
                p_chain = [(xp,1)]
        if rel==rels['attributive_adverbial'][1]:   #durative
            p_chain = [(xp,1,'DUR')]
        if rel==rels['attributive_adverbial'][2]:   #multiple durative
            p_chain = [(xp,1,'MDU')]
        if rel==rels['attributive_adverbial'][3]:   #distant
            p_chain = [(xp,1,'DIS')]
        if rel==rels['attributive_adverbial'][4]:   #adverbial-tautological
            p_chain = [(xp,1,'TAU')]
        if rel==rels['attributive_adverbial'][5]:   #subective-adverbial
            p_chain = [(xp,1,'SUB')]
        if rel==rels['attributive_adverbial'][6]:   #objective-adverbial
            p_chain = [(xp,1,'OBJ')]
        if rel==rels['attributive_adverbial'][7]:   #subjective-copredicative
            p_chain = [(xp,1,'SCO')]
        if rel==rels['attributive_adverbial'][8]:   #objective-copredicative
            p_chain = [(xp,1,'OCO')]
        if rel==rels['attributive_adverbial'][9]:   #restrictive
            p_chain = [(xp,1)]
        if rel==rels['attributive_adverbial'][10]:  #parenthetic(al)
            p_chain = [(xp,1,'PRN')]
        if rel==rels['attributive_adverbial'][11]:  #subordinative
            p_chain = [(xp,1,'SBO')]
        if rel==rels['attributive_adverbial'][12]:  #explanatory
            p_chain = [(xp,1,'XPN')]
        if rel==rels['attributive_adverbial'][13]:  #adjoining
            p_chain = [(xp,1,'DJN')]
        if rel==rels['attributive_adverbial'][14]:  #specifying
            p_chain = [(xp,1,'SPC')]

        if rel==rels['coordinative'][0]:            #coordinative
            p_chain = [(xp,1)]
        if rel==rels['coordinative'][1]:            #sentential-coordinative
            #p_chain = [('SS',1),(xp,1)]
            p_chain = [(xp,1)]
        if rel==rels['coordinative'][2]:            #coordinative-conjunction
            p_chain = [(xp,1)]
        if rel==rels['coordinative'][3]:            #multiple
            #p_chain = [(xp,1)]
            p_chain = []

        if rel==rels['auxiliary'][0]:               #analytical
            p_chain = [(xp,1)]
        if rel==rels['auxiliary'][1]:               #passive-analytical
            p_chain = [(xp,1)]
        if rel==rels['auxiliary'][2]:               #auxiliary
            p_chain = [(xp,1,'AXL')]
        if rel==rels['auxiliary'][3]:               #quantitative-auxiliary
            p_chain = []
        if rel==rels['auxiliary'][4]:               #correlative
            p_chain = [(xp,1)]
        if rel==rels['auxiliary'][5]:               #expletive
            p_chain = [(xp,1,'EXP')]
        if rel==rels['auxiliary'][6]:               #proleptic
            p_chain = [(xp,1,'PRL')]

        if rel=='NP2P':
            #p_chain = [(xp,1)]
            #p_chain = [(xp,1,str(dep['address'])[:-3])]
            p_chain = [(xp,1,str(dep['ctag']))]

    else:
        return 'Invalid flag!'
    output['p_chain'] = p_chain
    return output

if __name__ == "__main__":
    pass

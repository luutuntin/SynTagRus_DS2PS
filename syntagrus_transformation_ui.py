#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SynTagRus Tree Transformation GUI Module
alexluu@brandeis.edu

Reference:
http://www.nltk.org/_modules/nltk/draw/util.html
"""

from Tkinter import *
import tkMessageBox
import ttk
from nltk.draw.util import CanvasFrame
from nltk.draw.tree import TreeWidget
#from syntagrus_utils import load_data
from syntagrus_transformation import *
# 1: change_labels()
# 2: transform_relative_structures()
# 3: transform_np2p_structures()
# 4: transform_coordinative_structures()


#p_trees = load_data('p_trees.pkl')
#n2p_trees_temp = load_data('n2p_trees_temp.pkl')
#all_trees = p_trees + n2p_trees

class TTFrame():    # Tree Transformation Frame
    def __init__(self,parent=None,index=0,trees=list(),
                 readonly=False):
        self._trees = trees
        self._i_range = len(self._trees)
        self._bold = ('helvetica', -12, 'bold')
        self._helv = ('helvetica', -12)
        if parent is None:
            self._parent = Tk()            
        else:
            self._parent = parent
        t1 = 'Syntagrus - Brandeis - Tree Transformation'
        self._parent.title(t1)
        self._parent.columnconfigure(0,weight=1)
        self._parent.rowconfigure(0,weight=1)


        self._m_f = ttk.Frame(self._parent)
        self._m_f.grid(column=0,row=0,sticky=(N,W,E,S))
        self._m_f.columnconfigure(0,weight=1)
        self._m_f.rowconfigure(1,weight=1)


        self._i_f = ttk.Frame(self._m_f)
        self._i_f.grid(column=0,row=0,sticky=(N,W,E,S))
        self._i_f.columnconfigure(0,weight=1)
        self._i_f.columnconfigure(7,weight=1)

        self._o_p = ttk.Panedwindow(self._m_f,
                                    orient=VERTICAL)
        self._o_p.grid(column=0,row=1,sticky=(N,W,E,S))


        t2 = 'Please enter the index (0-' + \
             str(self._i_range-1) + ')'
        self._i_l = ttk.Label(self._i_f,text=t2)
        self._i_l.grid(column=1,row=0,columnspan=3,
                       sticky=(N,W,E,S))
        self._i_l['anchor'] = 'center'

        self._index = StringVar()
        self._index.set(index)
        self._i_e = ttk.Entry(self._i_f,width=5,
                              textvariable=self._index)
        self._i_e.grid(column=1,row=1,sticky=(N,W,E,S))
        if readonly:
            self._i_e['state']='readonly'

        self._i_b = ttk.Button(self._i_f,width=5,
                    text='Draw',command=self._draw)
        self._i_b.grid(column=3,row=1,sticky=(N,W,E,S))

        self._extra_label = ttk.Label(self._i_f,text='   ')
        self._extra_label.grid(column=4,row=0,rowspan=2,
                               sticky=(N,W,E,S))

        self._var_1 = IntVar()
        self._i_cb_1 = ttk.Checkbutton(self._i_f,
                       text='Transformation 1',
                       variable=self._var_1)
        self._i_cb_1.grid(column=5,row=0,sticky=(N,W,E,S))
        self._var_2 = IntVar()
        self._i_cb_2 = ttk.Checkbutton(self._i_f,
                       text='Transformation 2',
                       variable=self._var_2)
        self._i_cb_2.grid(column=5,row=1,sticky=(N,W,E,S))
        self._var_3 = IntVar()
        self._i_cb_3 = ttk.Checkbutton(self._i_f,
                       text='Transformation 3',
                       variable=self._var_3)
        self._i_cb_3.grid(column=6,row=0,sticky=(N,W,E,S))
        self._var_4 = IntVar()
        self._i_cb_4 = ttk.Checkbutton(self._i_f,
                       text='Transformation 4',
                       variable=self._var_4)
        self._i_cb_4.grid(column=6,row=1,sticky=(N,W,E,S))


        n = 250
        self._o_f_1 = ttk.Labelframe(self._o_p,
                      text='Original',width=n,height=n)
        self._o_f_2 = ttk.Labelframe(self._o_p,
                      text='Transformed',width=n,height=n)
        self._o_p.add(self._o_f_1)
        self._o_p.add(self._o_f_2)


        self._o_cf_1 = CanvasFrame(parent=self._o_f_1,
                                   width=n*2.5,height=n)
        self._o_cf_1.pack(expand=1,fill='both')
        self._o_cf_2 = CanvasFrame(parent=self._o_f_2,
                                   width=n*2.5,height=n)
        self._o_cf_2.pack(expand=1,fill='both')


        self._i_e.focus()
        self._parent.bind('<Return>',self._draw)
        self._parent.mainloop()



    def _draw_tree(self,cf,t):
        return TreeWidget(cf.canvas(),
                          t,
                          node_font=self._bold,
                          leaf_color='#008040',
                          node_color='#004080',
                          roof_color='#004040',
                          roof_fill='white',
                          line_color='#004040',
                          draggable=1,
                          leaf_font=self._helv) 

    def _draw(self,*arg):    
        self._o_cf_1.canvas().delete('all')
        self._o_cf_2.canvas().delete('all')    
        try:
            i = int(self._index.get())
            if i in range(self._i_range):
                original = self._draw_tree(self._o_cf_1,
                                           self._trees[i])
                self._o_cf_1.add_widget(original,10,10)
                if sum([self._var_1.get(),
                        self._var_2.get(),
                        self._var_3.get(),
                        self._var_4.get()]):
                    temp = deepcopy(self._trees[i])
                    if self._var_1.get():
                        change_label(temp,'SBD','SBAR')
                    if self._var_2.get():
                        transform_relative_structures(temp)
                    if self._var_3.get():
                        transform_np2p_structures(temp)
                    if self._var_4.get():
                        transform_coordinative_structures(temp)
                    transformed = self._draw_tree(self._o_cf_2,
                                                  temp)
                    self._o_cf_2.add_widget(transformed,10,10)
                    
            else:
                tkMessageBox.showinfo(message='Incorrect index!')
                self._index.set(0)
        except ValueError:
            pass

if __name__ == "__main__":
    ttframe=TTFrame(trees=trees_plus)

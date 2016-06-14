#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import tkMessageBox
import ttk
from nltk.draw.util import CanvasFrame
from nltk.draw.tree import TreeWidget
from time import sleep
from syntagrus_transformation_ui import TTFrame
from syntagrus_utils import load_data


p_graphs = load_data('p_graphs.pkl')
p_trees = load_data('p_trees.pkl')

n_graphs = load_data('n_graphs.pkl')
n2p_graphs_temp = load_data('n2p_graphs_temp.pkl')
n2p_trees_temp = load_data('n2p_trees_temp.pkl')

bold = ('helvetica', -12, 'bold')
helv = ('helvetica', -12)
def draw_tree(cf,t):
    return TreeWidget(cf.canvas(),t,node_font=bold,
           leaf_color='#008040',node_color='#004080',
           roof_color='#004040',roof_fill='white',
           line_color='#004040',draggable=1,leaf_font=helv) 

def draw(*arg):    
    d_cf.canvas().delete('all')
    p_cf.canvas().delete('all')
    i_b_2['state']='!disabled'
    flag = projectivity.get()
    if flag=='p':
        i_range = p_max + 1
    else:
        i_range = n_max + 1
    try:
        i = int(index.get())
        if i in range(i_range):
            if flag=='p':
                d_t = draw_tree(d_cf,p_graphs[i])
                d_cf.add_widget(d_t,10,10)
                p_t = draw_tree(p_cf,p_trees[i])
                p_cf.add_widget(p_t,10,10)
            else:    
                d_t_n = draw_tree(d_cf,n_graphs[i])
                d_cf.add_widget(d_t_n,10,10)            
                d_t_p = draw_tree(d_cf,n2p_graphs_temp[i])
                d_cf.add_widget(d_t_p,10,d_t_n.bbox()[3]+10)
                p_t = draw_tree(p_cf,n2p_trees_temp[i])
                p_cf.add_widget(p_t,10,10)
        else:
            tkMessageBox.showinfo(message='Incorrect index!')
            index.set(0)
    except ValueError:
        pass

def open_window():
    w = Toplevel(root)  #windows
    flag = projectivity.get()
    if flag=='p':
        ts = p_trees
    else:
        ts = n2p_trees
    ttframe = TTFrame(w,index.get(),ts)
    
def choose_p(*arg):
    max_index.set(p_max)

def choose_n(*arg):
    max_index.set(n_max)

root = Tk()
root.title("SynTagRus - Brandeis")
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)


m_f = ttk.Frame(root)
m_f.grid(column=0,row=0,sticky=(N,W,E,S))
m_f.columnconfigure(0,weight=1)
m_f.rowconfigure(1,weight=1)


i_f = ttk.Frame(m_f)
i_f.grid(column=0,row=0,sticky=(N,W,E,S))
i_f.columnconfigure(0,weight=1)
i_f.columnconfigure(8,weight=1)

o_p = ttk.Panedwindow(m_f,orient=HORIZONTAL)
o_p.grid(column=0,row=1,sticky=(N,W,E,S))


projectivity = StringVar()
projectivity.set('p')
i_rb_p1 = ttk.Radiobutton(i_f,text='projective',
                          variable=projectivity,value='p',
                          command=choose_p)
i_rb_n1 = ttk.Radiobutton(i_f,text='non-projective',
                          variable=projectivity,value='n',
                          command=choose_n)
i_rb_p1.grid(column=1,row=0,sticky=(N,W,E,S))
i_rb_n1.grid(column=1,row=1,sticky=(N,W,E,S))

t = 'Please enter the index - from 0 to'
i_l = ttk.Label(i_f,text=t)
i_l.grid(column=2,row=0,columnspan=5,sticky=(N,W,E,S))
i_l['anchor'] = 'center'

index = StringVar()
index.set(0)
i_e = ttk.Entry(i_f,width=5,textvariable=index)
i_e.grid(column=3,row=1,sticky=(N,W,E,S))

i_b_1 = ttk.Button(i_f,width=5,text='Draw',command=draw)
i_b_1.grid(column=5,row=1,sticky=(N,W,E,S))

max_index = StringVar()
p_max = len(p_trees)-1
n_max = len(n2p_trees_temp)-1
max_index.set(p_max)
i_rb_p2 = ttk.Radiobutton(i_f,text=str(p_max),
                         variable=max_index,value=p_max)
i_rb_n2 = ttk.Radiobutton(i_f,text=str(n_max),
                         variable=max_index,value=n_max)
i_rb_p2.grid(column=7,row=0,sticky=(N,W,E,S))
i_rb_n2.grid(column=7,row=1,sticky=(N,W,E,S))

i_b_2 = ttk.Button(i_f,width=5,text='Tree tranformation',
                   command=open_window)
i_b_2.grid(column=3,row=2,columnspan=3,sticky=(N,W,E,S))


n = 300
d_f = ttk.Labelframe(o_p,text='DS',width=n,height=n)
p_f = ttk.Labelframe(o_p,text='PS',width=n,height=n)
o_p.add(d_f)
o_p.add(p_f)


d_cf = CanvasFrame(parent=d_f,width=n,height=n)
d_cf.pack(expand=1,fill='both')
p_cf = CanvasFrame(parent=p_f,width=n,height=n)
p_cf.pack(expand=1,fill='both')


i_e.focus()
i_rb_p2['state']='disabled'
i_rb_n2['state']='disabled'
root.bind('<Return>',draw)
root.mainloop()

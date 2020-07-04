#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 20:55:04 2020

@author: ramandwivedi
"""


import sqlite3

def tool_transfer():
    con = sqlite3.connect('test.db')
    cur = con.cursor()
    city = input('selec city to transfer-> bombay, pune:\n')
    city = city.lower()
    tool_id = int(input('select tool id: '))
    quantity = int(input('enter quantity')) 
    cur.execute('select * from main where id = ?',(tool_id,))
    tool_info = cur.fetchone()
    avl_quant = tool_info[-1]
    if not avl_quant >= quantity:
        return
    tool_name = tool_info[-3]
    sr = tool_info[-2]
    sr = sr.split('_')
    sr = sr[0]+'_'+str((avl_quant-quantity)+1)
    if quantity <= avl_quant:
        cur.execute(f'update main set quantity = {avl_quant-quantity} where id = {tool_id}')
        cur.execute('insert into {0}(tool,sr_num,quantity) values("{1}","{2}",{3})'.format(city,tool_name,sr,quantity))
        cur.execute('select * from {0}'.format(city))
        print(cur.fetchall())
    con.commit()
    con.close()
        
tool_transfer()
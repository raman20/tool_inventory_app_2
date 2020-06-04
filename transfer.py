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
    cur.execute(f'select * from main where id = {tool_id}')
    tool_info = cur.fetchall()
    avl_quant = tool_info[0][-1]
    sr_num = tool_info[0][-2]
    sr_num = sr_num.split('_')
    sr_num = sr_num[0]+'_'+str((avl_quant-quantity)+1)
    if quantity <= avl_quant:
        cur.execute(f'update main set quantity = {avl_quant-quantity}')
        cur.execute(f'insert into {city}(sr_num,quantity) values({sr_num},quantity)')
        cur.execute(f'select * from {city}')
        print(cur.fetchall())
        
tool_transfer()
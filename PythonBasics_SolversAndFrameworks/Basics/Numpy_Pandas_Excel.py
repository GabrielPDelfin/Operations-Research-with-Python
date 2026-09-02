# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 19:36:29 2025

@author: penad
"""


import numpy as np
import pandas as pd
'''import temp

print(temp.my_function(1, 1))
print(temp.my_function(2, 3))
print(temp.my_function(5, 6))'''

ages = np.array([10,15,20,18])
marks = np.array([9,8,5,7])

#print(marks[ages>15])

df = pd.DataFrame({
    'name': ['a', 'b', 'a', 'c'],
    'mark': [10, 9, 8, 7]
    })

dataMarks = pd.read_excel('Book 2.xlsx', sheet_name='Hoja2', engine='openpyxl')
dataPeople = pd.read_excel('Book 2.xlsx', sheet_name='Hoja1', engine='openpyxl')

dataAll = dataMarks.set_index('name').join(dataPeople.set_index('name'))

marks = dataAll.groupby('name').mark.mean()

print(dataMarks)
print(dataPeople)
print(dataAll)
print(marks)

marks.to_excel('output.xlsx')
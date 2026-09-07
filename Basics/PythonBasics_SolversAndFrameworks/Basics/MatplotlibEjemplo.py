# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 02:32:22 2025

@author: penad
"""
import matplotlib.pyplot as plt

salaries = [10,12,12,17]
names = ['a','b','c','d']
plt.bar(names,salaries, color='red')

def max_odd(mylist):
    oddNumbers = [i if i%2==1 else 0 for i in mylist]
    
    print(oddNumbers)
    return max(oddNumbers)

print(max_odd([1,5,7,3,8,10,3,40,5]))
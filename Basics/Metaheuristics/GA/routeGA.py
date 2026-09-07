# -*- coding: utf-8 -*-

import numpy as np
from geneticalgorithm import geneticalgorithm as ga
import pandas as pd

dataNodos = pd.read_excel('route_inputs.xlsx', sheet_name='nodes', engine='openpyxl')
dataCaminos = pd.read_excel('route_inputs.xlsx', sheet_name='paths', engine='openpyxl')

varbounds = np.array([ [0,1] for camino in dataCaminos['node_from'] ])
vartype = np.array([ ['int'] for camino in dataCaminos['node_from'] ])

'''
nodosIn = {key:[] for key in dataNodos['node']}
nodosOut = {key:[] for key in dataNodos['node']}

for ruta in dataCaminos.iterrows():
    nodosIn[ruta[1]['node_to']].append(ruta[1]['node_from'])
    nodosOut[ruta[1]['node_from']].append(ruta[1]['node_to'])
'''

def count1_7(ruta, x, sumaNodo1, sumaNodo7):
    if(ruta[1]['node_from'] == dataNodos.loc[0, 'node']):
        if x[ruta[0]]  == 1:
            #Sumar 1
            sumaNodo1+=1
            
    if(ruta[1]['node_to'] == dataNodos.loc[6, 'node']):
        if x[ruta[0]]  == 1:
            #Sumar 1
            sumaNodo7+=1
    return sumaNodo1, sumaNodo7

def f(x):
    pen = 0
    
    comprobado = False
    
    sumaNodo1 = 0
    sumaNodo7 = 0
    
    #Comprobar nodos intermedios. El sumatorio de las rutas que contenga el nodo x como destino debe coincidir con el sumatorio de rutas qye contenga el nodo x como origen
    #Recorrer la lista de nodos intermedios, para cada nodo buscar los bits que tengan el nodo como destino y origen, comprobar si la suma de sus rutas coinciden.
    for nodo in dataNodos.iterrows():
        if nodo[1]['description'] == 'middle point':
            actual = nodo[1]['node']
            numOrigenes = 0
            numDestinos = 0
            for ruta in dataCaminos.iterrows():
                
                #Comprobar el primer y último nodo
                if not comprobado:
                    sumaNodo1, sumaNodo7 = count1_7(ruta, x, sumaNodo1, sumaNodo7)   
                            
               
                
                #Contar las veces que el nodo actual se incluya en una ruta
                if ruta[1]['node_to'] == actual:
                    if x[ruta[0]]  == 1:
                        numDestinos+=1
                if ruta[1]['node_from'] == actual:
                    if x[ruta[0]]  == 1:
                        numOrigenes+=1
            
            if sumaNodo1 != 1 and not comprobado:
                pen = np.inf
                break
            if sumaNodo7 != 1 and not comprobado:
                pen = np.inf
                break
            
            comprobado = True
            
            if not(numOrigenes == numDestinos == 1) and not(numOrigenes == numDestinos == 0):
                pen = np.inf
                break
                
                
        
        
    return (sum(
        [x[i]*dataCaminos.loc[i, 'distance'] for i in range(0,len(dataCaminos))]
        )) + pen
#print(f([0,1,0,0,0,0,1,1]))

algorithm_param = {'max_num_iteration': 100,\
                   'population_size':100,\
                   'mutation_probability':0.1,\
                   'elit_ratio': 0.01,\
                   'crossover_probability': 0.5,\
                   'parents_portion': 0.3,\
                   'crossover_type':'uniform',\
                   'max_iteration_without_improv':None}

model = ga(function=f,dimension=len(dataCaminos),variable_type_mixed=vartype,variable_boundaries=varbounds,algorithm_parameters=algorithm_param)

model.run()

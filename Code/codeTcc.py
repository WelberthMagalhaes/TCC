import pandas as pd
from problema import Problema
import numpy as np
from mip import *

entrada = Problema('C:/Users/wheidermagal/OneDrive - DXC Production/Documents/Pessoal/TCC/inputs/input.xls')

# ENTRADAS
N = entrada.N
T = int(entrada.T)
c = entrada.ci
h = entrada.hi

m = Model("MIN custos totais") # Nome do modelo

x = {(i, j): m.add_var(obj=0, var_type=INTEGER, name="x(%s,%d)" % (i, j))
	for i in N 
		for j in range(1,T+1)}

y = {(i, j): m.add_var(obj=0, var_type=INTEGER, name="y(%s,%d)" % (i, j))
	for i in N
		for j in range(1,T+1)}


m.objective = minimize( xsum((c[i] * x[i,j]) + (h[i]*y[i,j]) for i in N for j in range(1,T+1)))

#acessar variável
print(x['a1',1])
m.write("teste.lp")

#print("Conjunto de Toners:"+str(entrada.N))







#print("Volume ocupado pelo toner i:")
#for toner, volume in entrada.vi.items():
#	print(toner, volume)

#print(entrada.dit['b1'][0])

"""	
print("Conjunto de Toners:"+str(entrada.N))
print("Períodos:"+str(entrada.T))
print("Armazenamento:"+str(entrada.A))
print("Volume ocupado pelo toner i:")
for toner, volume in entrada.vi.items():
	print(toner, volume)
print("*------------------------------*")
print("Margem minima:")
for toner, margem in entrada.eit.items():
	print(toner, margem)
print("*------------------------------*")
print("Demanda esperada:")
for toner, demanda in entrada.dit.items():
	print(toner, demanda)
print(entrada.dit['b1'][1])
print("*------------------------------*")
print("Estoque inicial:")
for toner, einicial in entrada.sit.items():
	print(toner, einicial)
print("*------------------------------*")
print("Custo de capital:")
for toner, custo in entrada.hi.items():
	print(toner, custo)
print("*------------------------------*")
print("Custo unitário de cada toner:")
for toner, custounit in entrada.ci.items():
	print(toner, custounit)
print("*------------------------------*")
print(entrada.ci.get('b2'))

"""

	# busca:  dit['a1'][0 ou 1]

	#retornar as demandas média esperadas
	#for i in N
	#	print(dit[i])
	#se tiver histórico anual fazer a média e desvio padrão entre os meses
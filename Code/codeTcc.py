from xml.sax.handler import EntityResolver
from openpyxl import Workbook
import pandas as pd
from problema import Problema
import numpy as np
from mip import *
import openpyxl
import string

entrada = Problema('C:/Users/wheidermagal/OneDrive - DXC Production/Documents/Pessoal/TCC/inputs/input.xls')
def gravaResultado():
	qtdCompradaX = pd.DataFrame(index=N, columns=range(1,T))
	qtdEstocadaY = pd.DataFrame(index=N, columns=range(1,T))
	for t in range(1,T):
		for i in N:
			qtdCompradaX.at[i,t] = x[i,t].x
			qtdEstocadaY.at[i,t] = y[i,t].x

	qtdCompradaX.to_excel('x.xlsx')
	qtdEstocadaY.to_excel('y.xlsx')

# ENTRADAS
N = entrada.N
T = int(entrada.T+1)
c = entrada.ci
h = entrada.hi
s = entrada.si
d = entrada.di
e = entrada.ei
v = entrada.vi
A = entrada.A

m = Model("MIN custos totais") # Nome do modelo

x = {(i, j): m.add_var(obj=0, var_type=INTEGER, name="x(%s,%d)" % (i, j))
	for i in N 
		for j in range(T)}

y = {(i, j): m.add_var(obj=0, var_type=INTEGER, name="y(%s,%d)" % (i, j))
	for i in N
		for j in range(T)}


m.objective = minimize( xsum((c[i] * x[i,j]) + (h[i]*y[i,j]) for i in N for j in range(T)))

# Restrição 1: Insere o estque inicial
for i in N:
	m += y[i,0] == s[i]

# Restrição 2: equaliza o estoque. Estoque atual = estoque inicial + Qtd comprada - demanda
# no modelo está excluindo o 0 do conjunto N. Não teria que excluí-lo do T?
for i in N:
	for t in range(1,T):
		m += y[i,t] == y[i,t-1] + x[i,t] - d[i][t-1]

# Restrição 3: exige que a quantidade armazenada seja igual ou maior o estoque de segurança
for i in N:
	for t in range(1,T):
		m += y[i,t] >= e[i]

# Restrição 4: exige que o volume de toner armazenado seja menor ou igual ao espaço para armazenamento
m += (xsum( y[i,t] * v[i] for i in N for t in range(1,T)))<= A

# Restrição 5: Quantidade comprada não pode ser menor que zero
for i in N:
	for t in range(1,T):
		m += x[i,t] >=0


m.optimize()

m.write("teste.lp")
m.write("solucao.sol")
gravaResultado()

#acessar variável
#print(x['a1',0])

#print("X:"+"\n" + str(qtdCompradaX.head))
#print("Y:"+"\n" + str(qtdEstocadaY.to_string))

#qtdCompradaX.to_csv('x.csv')
#qtdEstocadaY.to_csv('y.csv')

#TODO analisar se o resultado faz sentido; criar alguma visualização; pensar em gerar novas instâncias aleatórias
#range(0.2, 0.7)*




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
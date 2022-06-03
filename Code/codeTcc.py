from xml.sax.handler import EntityResolver
from openpyxl import Workbook
import pandas as pd
from problema import Problema
import numpy as np
from mip import *
import openpyxl
import string


entrada = Problema('C:/Users/wheidermagal/OneDrive - DXC Production/Documents/Pessoal/TCC/inputs/input1.xlsx')
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


m.objective = minimize( xsum((c[i][j-1] * x[i,j]) + (h[i][j-1]*y[i,j]) for i in N for j in range(T)))

# Restrição 1: Insere o estque inicial
for i in N:
	m += y[i,0] == s[i]

# Restrição 2: equaliza o estoque. Estoque atual = estoque inicial + Qtd comprada - demanda
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
m.write("solucao.sol")
m.write("teste.lp")

gravaResultado()
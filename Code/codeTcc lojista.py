import pandas as pd
from problema import Problema
from mip import *

# entrada = Problema('inputs/input.xlsx')
# entrada = Problema('inputs/input-sem-estoque-inicial.xlsx')
entrada = Problema('inputs/Graficos/aleatorio-20-toners-24-meses.xlsx')
def gravaResultado():
	qtdCompradaX = pd.DataFrame(index=N, columns=range(1,T+1))
	qtdEstocadaY = pd.DataFrame(index=N, columns=range(1,T+1))
	for t in range(1,T+1):
		for i in N:
			qtdCompradaX.at[i,t] = x[i,t].x
			qtdEstocadaY.at[i,t] = y[i,t].x

	qtdCompradaX.to_excel('x.xlsx')
	qtdEstocadaY.to_excel('y.xlsx')

# ENTRADAS
N = entrada.N
T = entrada.T
c = entrada.ci
h = entrada.hi
s = entrada.si
d = entrada.di
e = entrada.ei
v = entrada.vi
A = entrada.A

m = Model("MIN custos totais", solver_name="CBC") # Nome do modelo

x = {(i, j): m.add_var(obj=0, var_type=INTEGER, lb=0.0, name="x(%s,%d)" % (i, j)) for i in N for j in range(1, T+1)}

y = {(i, j): m.add_var(obj=0, var_type=INTEGER, lb=0.0, name="y(%s,%d)" % (i, j)) for i in N for j in range(0, T+1)}

m.objective = minimize( xsum((c[i][j-1] * x[i,j]) + (h[i][j-1]*y[i,j]) for i in N for j in range(1, T+1)))
# m.objective = minimize( xsum((c[i][j-1] * x[i,j]) for i in N for j in range(1, T+1)))

# Restrição 1: Insere o estque inicial
for i in N:
	m.add_constr(y[i,0] == s[i], name="estq_ini(%s)" % i)

# Restrição 2: equaliza o estoque. Estoque atual = estoque anterior + Qtd comprada - demanda
for i in N:
	for t in range(1,T+1):
		m.add_constr(y[i,t] == y[i,t-1] + x[i,t] - d[i][t-1], name="calc_estq(%s,%d)" % (i,t))

# Restrição 3: exige que a quantidade armazenada seja maior ou igual do que o estoque de segurança
for i in N:
	for t in range(1,T+1):
		m.add_constr(y[i,t] >= e[i], name="estq_seg(%s,%d)" % (i,t))

# Restrição 4: exige que o volume de toner armazenado seja menor ou igual ao espaço para armazenamento
for t in range(1,T+1):
	m.add_constr(xsum(y[i,t] * v[i] for i in N) <= A, name="cap_tempo(%d)" % (t))

#restrição para garantir que a quantidade comprada seja igual a demanda
aux = s
for i in N:
	if (aux[i] >= (d[i][0] + e[i])):
		x[i,1].lb = x[i,1].ub = 0.0
		aux[i] = aux[i] - d[i][0] - e[i]
	else:
		x[i,1].lb = x[i,1].ub = d[i][0] + e[i] - aux[i]
		aux[i] = 0

	for j in range(2, T+1):
		if (aux[i] >= d[i][j-1]):
			x[i,j].lb = x[i,j].ub = 0.0
			aux[i] = aux[i] - d[i][j-1]
		else:
			x[i,j].lb = x[i,j].ub = d[i][j-1] - aux[i]
			aux[i] = 0
			

m.write("modelo.lp")
m.optimize()
m.write("solucao.sol")

gravaResultado()
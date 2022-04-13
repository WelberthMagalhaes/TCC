from mip import Model, xsum, maximize, BINARY


#// dados de entrada colocar em csv e carregar o arquivo

p = [10, 13, 18, 31, 7, 15]     
w = [11, 15, 20, 35, 10, 33]
c, I = 47, range(len(w))

#---


m = Model("knapsack")   // nome do modelo para instanciar

x = [m.add_var(var_type=BINARY) for i in I] # BINARY por INTEGER

m.objective = maximize(xsum(p[i] * x[i] for i in I)) # maximize por minimize

m += xsum(w[i] * x[i] for i in I) <= c   # inserindo restrição

m.optimize()

selected = [i for i in I if x[i].x >= 0.99]
print("selected items: {}".format(selected)) # imprimir estoque e quantidade comprada




#1- criar o arquivo para o python
#2- ler o arquivo criando os conjuntos
#3- margem minima media item/periodo (estoque de seguranca) = lista de lista
#4- demando item/periodo = lista de lista


#  https://www.hashtagtreinamentos.com/ler-arquivo-excel-varias-abas-no-python


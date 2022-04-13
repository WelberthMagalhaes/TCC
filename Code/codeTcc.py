import pandas as pd
from Code.problema import Problema
import numpy as np


#criar classe entrada no dessa função
entrada = Problema('/content/drive/MyDrive/Colab Notebooks/input.xls')

df = pd.read_excel("x", sheet_name=0)
	
entrada.getN

#def conjuntos: -> passar para classe Problema tudo abaixo
	
	df = pd.read_excel("/content/drive/MyDrive/Colab Notebooks/input.xls", sheet_name=0)
	
	# N - Conjunto de Toners #Validado 16/12
	aux = df.columns.to_list()
	aux.pop(0)
	N = aux
	#-------------

	# T - Número de períodos #Validado 16/12
	T = df.iat[3,1] 
	#-------------

	# A - Capacidade de Armazenamento #Validado 16/12
	A = df.iat[5,1]
	#-------------
	
	# si - Estoque Inicial
	
	#-------------

	# vi - Volume ocupado por cada toner #Validado 16/12
	df = pd.read_excel("/content/drive/MyDrive/Colab Notebooks/input.xls", sheet_name=1)

	vi = list(df['Volume'])
	#-------------

	# eit - margem mínima média do toner i no período t (estoque de segurança) #Validado 16/12
	df = pd.read_excel("/content/drive/MyDrive/Colab Notebooks/input.xls", sheet_name=2)

	eit = {df.values[i][0] : df.values[i][1] for i in range(df['toner'].size)}


	#-------------

	# dit demanda média esperada do toner i no período t  #Validado 16/12

	df = pd.read_excel("/content/drive/MyDrive/Colab Notebooks/input.xls", sheet_name=3)

	dit = {df.values[i][0] : df.values[i][1:] for i in range(df['toner'].size)}

	# busca:  dit['a1'][0 ou 1]

	#retornar as demandas média esperadas
	#for i in N
	#	print(dit[i])
	#se tiver histórico anual fazer a média e desvio padrão entre os meses
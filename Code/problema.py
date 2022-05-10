from pprint import pp
import pandas as pd
import numpy as np


class Problema:
		
	def __init__(self, arq):
		
		#leitura do arquivo
		df = pd.read_excel(arq, sheet_name=0)

		# N - Conjunto de Toners
		aux = df.columns.to_list()
		aux.pop(0)
		self.N = aux
		#--------------------

		# T - Número de períodos
		self.T = df.iat[3,1] 
		#--------------------

		#indice de coluna para custo e demanda de toner
		#col = int(self.T+1)

		# A - Capacidade de Armazenamento
		self.A = df.iat[5,1]
		#--------------------

		#si - Estoque inicial do toner i
		s = df
		s = s.T
		s = s.drop('Conjunto de Toners')
		s = s.drop(columns=0)
		ind = s.index.to_list()
		self.si = {ind[i] : s.values[i][0] for i in range(s[1].size)}
		#--------------------

		# ci - Custo unitário do toner i
		df = pd.read_excel(arq, sheet_name=5)
		col = int(self.T+1)
		self.ci = {df.values[i][0] : df.values[i][1:col] for i in range(df['toner'].size)}

		"""c = df
		c = c.dropna()
		c = c.drop(1)
		c = c.T
		c = c.drop('Conjunto de Toners')
		ind = c.index.to_list()
		self.ci = {ind[i] : c.values[i][0] for i in range(c[0].size)}"""

		#--------------------

		# vi - Volume ocupado por cada toner #Validado 16/12
		df = pd.read_excel(arq, sheet_name=1)
		self.vi = {df.values[i][0] : df.values[i][1] for i in range(df['toner'].size)}
		#--------------------

		# ei - margem mínima média do toner i no período t (estoque de segurança) #Validado 16/12
		df = pd.read_excel(arq, sheet_name=2)
		self.ei = {df.values[i][0] : df.values[i][1] for i in range(df['toner'].size)}
		#--------------------
		
		# dit - demanda média esperada do toner i no período t  #Validado 16/12
		df = pd.read_excel(arq, sheet_name=3)
		col = int(self.T+1)
		self.di = {df.values[i][0] : df.values[i][1:col] for i in range(df['toner'].size)}
		#--------------------

		# hi - Custo de capital do estoque por unidade do toner i
		df = pd.read_excel(arq, sheet_name=4)
		self.hi = {df.values[i][0] : df.values[i][1] for i in range(df['toner'].size)}
		#--------------------
class Problema:
	
	def __init__(self, arq):
		
		#leitura do arquivo
		df = pd.read_excel("/content/drive/MyDrive/Colab Notebooks/input.xls", sheet_name=0)

		# N - Conjunto de Toners
		aux = df.columns.to_list()
		aux.pop(0)
		self.N = aux
		#--------------------

		# T - Número de períodos
		self.T = df.iat[3,1] 
		#--------------------

		# A - Capacidade de Armazenamento
		self.A = df.iat[5,1]
		#--------------------
		
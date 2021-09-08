import json
import yaml

class FileParser:
	'''
	Classe para processar os ficheiros de config. Tenta fazer o parse entre todos os parsers possiveis
	até que um retorne alguma coisa. Se nenhum retornar, o ficheiro está mal formatado.
	'''
	def __init__(self):
		self.parsers = [JSONParser(), YAMLParser()]		#adicionar outros parsers

	def parse(self,path):
		for p in self.parsers:
			output = p.parse(path)
			if output:
				return output

		return None
	
class JSONParser(FileParser):
	def __init__(self):
		pass

	def parse(self, path):
		fp = open(path, 'r')

		try:
			data = json.load(fp)
		except json.JSONDecodeError:
			data = None
		fp.close()
		return data

class YAMLParser(FileParser):
	def __init__(self):
		pass

	def parse(self, path):
		fp = open(path, 'r')
		try:
			data = yaml.load(fp, Loader=yaml.FullLoader)
		except yaml.scanner.ScannerError:
			data = None
		fp.close()
		return data

'''
class OutroParser(FileParser):

	Função parse tem que retornar um dicionário.
	def parse(self,path):
		...
'''




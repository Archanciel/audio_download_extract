import json
import os


class BaseInfoDic:
	"""
	This base class contains code used in its sub-classes.
	"""
	DIC_FILE_NAME_EXTENT = '_dic.txt'
	
	def __init__(self):
		self.dic = None
	
	def _loadDicIfExist(self, dicFilePathName):
		"""
		If a file containing the dictionary data for the corresponding playlist
		exists, it is loaded using json.
		
		:param dicFilePathName:
		
		:return None or loaded dictionary
		"""
		dic = None

		if os.path.isfile(dicFilePathName):
			with open(dicFilePathName, 'r') as f:
				dic = json.load(f)

		return dic
	
	def __str__(self):
		try:
			return json.dumps(self.dic, sort_keys=False, indent=4)
		except Exception as e:
			print(e)

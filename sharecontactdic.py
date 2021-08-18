import json

CONTACT_NAME_KEY = 'name'
CONTACT_EMAIL_KEY = 'email'
CONTACT_PHONE_NUMBER_KEY = 'phoneNumber'

class ShareContactDic():
	def __init__(self, dicPathFileName):
		self.loadDic(dicPathFileName)
	
	def loadDic(self, dicPathFileName):
		self.dic = None
		
		try:
			with open(dicPathFileName, 'r') as f:
				self.dic = json.load(f)
		except Exception as e:
			print(e)

	def saveDic(self, dicPathFileName, contactDicList):
		self.dic = {}
		i = 1
		
		for contactDic in contactDicList:
			self.dic[str(i)] = contactDic
			i += 1
			
		with open(dicPathFileName, 'w') as f:
			try:
				json.dump(self.dic,
						  f,
						  indent=4,
						  sort_keys=True)
			except Exception as e:
				print(e)


if __name__ == "__main__":
	dataDir = 'D:\\Development\\Python\\audiodownload\\test\\testData\\'
	dataFileName = "shareContacts.txt"
	dataFilePathName = dataDir + dataFileName
	scd = ShareContactDic(dataFilePathName)
	print(scd.dic)
	
	contactDicList = [{CONTACT_NAME_KEY: 'Jean-Pierre Schnyder',
					   CONTACT_EMAIL_KEY: 'jp.schnyder@gmail.com',
					   CONTACT_PHONE_NUMBER_KEY: '+41768224987'},
					  {CONTACT_NAME_KEY: 'Tamara Jagne',
					   CONTACT_EMAIL_KEY: 'tamara.jagne@gmail.com',
					   CONTACT_PHONE_NUMBER_KEY: '+41764286884'}
					 ]

	scd.saveDic(dataFilePathName, contactDicList)
import os, pickle
from configobj import ConfigObj

class ConfigManager:
	def __init__(self, configFilePathName):
		self.config = ConfigObj(configFilePathName)

		if len(self.config) == 0:
			raise FileNotFoundError(configFilePathName + " does not exist !")

	def getEmailDic(self):
		return self.config['mailTo']
		
	def getEmailLst(self): 
		emailDic = self.getEmailDic()
		emailNb = len(emailDic.keys())
		emailLst = []
	
		for i in range(1, emailNb + 1):
			key = str(i)
			email = emailDic[key]
			email = [key, email[0], email[1]]
			emailLst.append(email)
			
		return emailLst
				
if __name__ == '__main__':
	if os.name == 'posix':
		configFilePathName = '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/OrderMedic/ordermedic.ini'
	else:
		configFilePathName = 'D:\\Development\\Python\\OrderMedic\\ordermedic.ini'

	cm = ConfigManager(configFilePathName)
	
	for med in cm.getOrderedMedLst():
		print(med[0], ' ', med[1], ' ', med[2], ' ', med[3])



import unittest
import os, sys, inspect
from os.path import sep


currentDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentDir = os.path.dirname(currentDir)
sys.path.insert(0, parentDir)

from sharecontactdic import *
from dirutil import DirUtil

class TestShareContactDic(unittest.TestCase):
	def testSaveLoadDic(self):
		dataFileName = "shareContacts.txt"

		dataFilePathName = DirUtil.getTestAudioRootPath() + sep + dataFileName

		# emptying share contact dic file
		
		with open(dataFilePathName, 'w') as f:
			f.write('')

		scd = ShareContactDic(dataFilePathName)
		
		self.assertIsNone(scd.dic)

		# saving filled share contact dic file
		
		contactDicList = [{CONTACT_NAME_KEY: 'Jean-Pierre Schnyder',
		                   CONTACT_EMAIL_KEY: 'jp.schnyder@gmail.com',
		                   CONTACT_PHONE_NUMBER_KEY: '+41768224987'},
		                  {CONTACT_NAME_KEY: 'Tamara Jagne',
		                   CONTACT_EMAIL_KEY: 'tamara.jagne@gmail.com',
		                   CONTACT_PHONE_NUMBER_KEY: '+41764286884'}
		                  ]
		
		scd.saveDic(dataFilePathName, contactDicList)
		
		self.assertEqual('jp.schnyder@gmail.com', scd.dic['1'][CONTACT_EMAIL_KEY])
		self.assertEqual('Tamara Jagne', scd.dic['2'][CONTACT_NAME_KEY])
		self.assertEqual('+41764286884', scd.dic['2'][CONTACT_PHONE_NUMBER_KEY])


if __name__ == '__main__':
	unittest.main()
#	tst = TestShareContactDic()
#	tst.testLoadDic()

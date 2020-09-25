import sys, argparse

from constants import *
from configmanager import ConfigManager

class Requester:
	def __init__(self, configManager):
		self.configManager = configManager
		
	def getProjectName(self, commandLineArgs=None):
		"""
		Unless a command line arg is available this method ask the user to 
		select the project on which to apply the Transfer Files utility.
		
		@param commandLineArgs: used for unit testing only
		
		@return: selected project name or None if user entered Q for quit
		"""
		if commandLineArgs == None:
			# we are not unit testing ...
			commandLineArgs = sys.argv[1:]

		if commandLineArgs != []:
			projectName = self.decodeCommandLineArgs(commandLineArgs)
		else:
			projectNameList = [x for x in self.configManager.projects]
			userPrompt = "Select project (Q or Enter to quit):\n\n"
			
			for (i, projectName) in enumerate(projectNameList): 
				userPrompt += str(i + 1) + ' ' + projectName + '\n'
				
			userPrompt += '\n'

			selection = '-1'
			projectName = ''

			while int(selection) <= 0:
				selection = input(userPrompt).upper()
				
				if selection == 'Q' or selection == '':
					return None
					
				try:
					if int(selection) <= 0:
						userPrompt = self.addErrorToUserPrompt(userPrompt)
					else:
						try:
							projectName = projectNameList[int(selection) - 1]
						except:
							userPrompt = self.addErrorToUserPrompt(userPrompt)
							selection = -1
				except ValueError as e:
					userPrompt = self.addErrorToUserPrompt(userPrompt)
					selection = -1
								
		return projectName

	def getCreateCloudFolderConfirmation(self, folderName):
		"""
		This method ask the user if a new cloud directory has to be created
		or not. The method is called the very first time a project is handled
		by the Transfer Files utility. This is useful to enable the user to
		make sure the project name as defined in the local configuration file
		is correct, since the cloud dir is named with the project name.
		
		@param folderName: name of cloud dir, same as project name
		"""
		questionStr = 'Cloud project directory {} does not exist and will be created'.format(folderName)
		userPrompt = '\n' + questionStr + '.\n\nContinue (Y/N) '
		userChoice = input(userPrompt).upper()
		
		if userChoice == 'Y':
			return True
		else:
			return False
										
	def getUserConfirmation(self, questionStr, fileNameLst=[], filePathNameLst=[]):
		"""
		This method handles user confirmation in case of both uploading localy
		modified files to the cloud and downloading files from the cloud.
		
		In case of modified files upload, the user has several choices:
			
			o he can approve the upload
			o he can ask to list the modified files with their path
			o he can choose to update the last synch time
		
		In case of downloading files from the cloud, the user can simply 
		accept the download and move to the correct dirs. In case he refuses
		the download, he will then have the possibility to upload modified
		files instead. This enables the user to upload files, then modify
		additional or same files and upload or re-upload them on the cloud.
			
		@param questionStr:
		@param fileNameLst:
		@param filePathNameLst:
			
		@return: True and '' for new synch time if user confirms files upload
				 False and '' for new synch time if user cancels files upload
				 False and new synch time answer if user wants to update the
				 project synch time without uploading any file.
		"""
		if filePathNameLst != []:
			# this means that the method is called in order to upload files to
			# the cloud and not when asking to confirm downloading files from
			# the cloud. In this situation, it may be useful for the user to
			# see the path of the files which are candidates for upload, not
			# only their names.
			#
			# Additionally, the user has the possibility to update the last
			# synch time of the project.
			userPrompt = self.addFilesToUserPrompt(questionStr, fileNameLst, path='/P', upload='/U')
			userChoice = input(userPrompt).upper()
			
			if 'P' in userChoice:
				questionStr = questionStr.replace('P to display the path and ', '')	
				userPrompt = self.addFilesToUserPrompt(questionStr, filePathNameLst,path='', upload='/U')
			else:
				return self.handleUserChoice(userChoice)
		elif fileNameLst != []:
			# here, we are prompting for downloading files from the cloud
			userPrompt = self.addFilesToUserPrompt(questionStr, fileNameLst)
		else:
			# here, neither modified files upload nor cloud files download is adequate. We give
			# the user the possibility to update the last synch time
			userPrompt = self.addFilesToUserPrompt(questionStr, fileNameLst, upload='/U')
		
		userChoice = input(userPrompt).upper()
					
		return self.handleUserChoice(userChoice)

	def handleUserChoice(self, userChoice):
		"""
		This method determines if the user choosed to upload the modified files,
		to stop the utility or to update the last synch time in the local config
		file.
		
		@param userChoice: the letter the user typed when prompted
		
		@return: True or False for upload confirmation and last synch time
				 update value if any
		"""
		if 'U' in userChoice:
			return False, self.askUserNewSyncTime()
		elif userChoice == 'Y':
			return True, ''
		else:
			return False, ''
		
	def addFilesToUserPrompt(self, questionStr, fileNameLst, path='', upload=''):
		"""
		This method adds upload or download file names to the user prompt.
		
		@param questionStr: the question displayed to the user
		@param fileNameLst: file names to print before asking the question
		@param path: either empty or '/P'
		@param upload: either empty or '/U'
		
		@return: the full user prompt
		"""
		userPrompt = '\n'
				
		for fileName in fileNameLst:
			if DIR_SEP in fileName:
				# here, the file name is in fact a fuLl file path name. In order
				# to display a more readable file list, only the last 4 file
				# pathename element are kept
				filePathNameElementLst = fileName.split(DIR_SEP)[-4:]
				fileName = DIR_SEP.join(filePathNameElementLst)
 
			userPrompt += fileName + '\n'

		if fileNameLst == []:
			# here, neither modified files upload nor cloud files download is adequate. We give
			# the user the possibility to update the last synch time
			userPrompt += '\n' + questionStr + '.\n\nContinue (Q{}) '.format(upload)
		else:
			userPrompt += '\n' + questionStr + '.\n\nContinue (Y/N{}{}) '.format(path, upload)

		return userPrompt
	
	def addErrorToUserPrompt(self, userPrompt):
		"""
		This method ensures that 'Invalid selection. ' is put only once in the
		user prompt, at its beginning.
		
		@param userPrompt: current user prompt
		
		@return: updated user prompt
		"""
		userPrompt = userPrompt.replace('Invalid selection. ', '')
		userPrompt = 'Invalid selection. ' + userPrompt
		
		return userPrompt
		
	def askUserNewSyncTime(self):
		"""
		This method prompts the user for setting a new last synch time in the
		local config file.
		
		@return: the user choice for updating the last synch time. Possible
				 values are '' (Enter) for no change, 'N' for Now and a
				 dd/mm/yyyy hh:mm:ss specified date time value
		"""
		userPrompt = '\nUpdating the project last synch time.\nType Enter to leave it unchanged, N to update it to Now and\ndd/mm/yy or dd/mm/yy hh:mm:ss to fully specify the date '

		return input(userPrompt).upper()
				
	def decodeCommandLineArgs(self, argList):
		"""
		 This method ses argparse to acquire the user optional command line 
		 arguments.

		:param argList: were acquired from sys.argv or set by test code
		
		:return: document name (may be None), insertion point and image numbers list to add/insert
		"""
		parser = argparse.ArgumentParser(
			description="Version {}. The TransferFiles utility is used to transfer files from " \
						"one device to another device using the cloud as intermediary location. " \
						"What makes TransferFiles unique is that the directory structures on both " \
						"source target devices can be different. A local configuration file " \
						"(transfiles.ini) stores the information required for the transfer to " \
						"be done correctly. " \
						"TransferFiles can be used with or without command line parameters. " \
						"Without using the -p parameter to specify the project name (which " \
						"corresponds to the project section in " \
						"the configuration file), a menu listing the projects defined in the config " \
						"file is displayed in order for the user to select the project to which the " \
						"transfer is applied. ".format(VERSION_NUMBER)
		)

		parser.add_argument("-p", nargs="?", help="project name as defined in the configuration file.")

		args = parser.parse_args(argList)

		return args.p
		
if __name__ == "__main__":
	configManager = ConfigManager(CONFIG_FILE_PATH_NAME)
	rq = Requester(configManager)
	projectName = rq.getProjectName(None)
	print('\n' + projectName)

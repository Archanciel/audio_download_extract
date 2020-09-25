import pickle, os, os.path

if os.name == 'posix':
	FILE_PATH='/sdcard/transfiles.bin'
else:
	FILE_PATH='C:\\temp\\transfiles.bin'

DIC = {'dropboxApiKey':'Api key stored where you store passwords'}

def storeDicInBinFile():
	if os.path.exists(FILE_PATH):
		print(FILE_PATH + ' already exists. To avoid overwriting it by error, delete it manually first !')
		return
	
	with open(FILE_PATH, 'wb') as handle:
		pickle.dump(DIC, handle)   
		 
	with open(FILE_PATH, 'rb') as handle:
		b = pickle.loads(handle.read())
    
	print(b['dropboxApiKey'])
	
if __name__ == '__main__':
	storeDicInBinFile() 

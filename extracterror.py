class ExtractError:
	ERROR_TYPE_EXTRACT_TIME_GREATER_THAN_DURATION = 1

	def __init__(self, errorType, errorMsg):
		self.errorType = errorType
		
		if errorType == ExtractError.ERROR_TYPE_EXTRACT_TIME_GREATER_THAN_DURATION:
			if errorMsg == '':
				self.errorMsg = "extract time outside audio file duration.\nextraction ignored."
			else:
				self.errorMsg = "{}\nextract time outside audio file duration.\nextraction ignored.".format(errorMsg)

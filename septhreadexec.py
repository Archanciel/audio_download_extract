import threading, time


class SepThreadExec:
	"""
	This class executes on a separate thread the passed func. If the passed
	endFunc is not None, it will be executed on the same separated thread
	after the passed func is terminated.
	"""
	
	def __init__(self,
	             callerGUI,
	             func,
	             endFunc=None,
	             funcArgs=None,
	             endFuncArgs=None):
		"""
		Ctor.

		:param callerGUI:   GUI class which instantiate the class
		:param func:        function executed on the separated thread
		:param endFunc:     optional function executed on the separated thread
							once the func is executed
		:param funcArgs:    parm name: value dic. Ex: {'age': 25, 'name': 'Joe'}
		:param endFuncArgs: parm values tuple. Ex: (25, 'Joe') or (25, )
		"""
		self.callerGUI = callerGUI
		
		if endFuncArgs is None:
			endFuncArgs = ()
		if funcArgs is None:
			funcArgs = {}
		
		args = (func, endFunc) + endFuncArgs
		
		def _callback(func, endFunc, *a, **kw):
			"""
			WARNING:    def _callback(func, endFunc, **a, **kw): causes error
						'multiple **parameters are not allowed

			:param func:
			:param endFunc:
			:param a:       tuple containing parms values for the passed endFunc
			:param kw:      dic containing parms name values for the passed func
			"""
			func(**kw)
			
			if endFunc is not None:
				endFunc(*a)
		
		self.t = threading.Thread(target=_callback, args=args, kwargs=funcArgs)
		self.t.setName('Exec thread ' + self.t.getName())
		self.t.daemon = True
	
	def start(self):
		self.t.start()


if __name__ == "__main__":
	class GuiStub:
		def myFunc(self, name='', age=0):
			for i in range(5):
				time.sleep(1)
				print('My name is {}. I am {} years old'.format(name, age))
		
		def myEndFunc(self, name='', age=0):
			print('MY SURNAME WAS {}. I was {} years old'.format(name.upper(), age))
	
	
	guiStub = GuiStub()
	ste = SepThreadExec(callerGUI=guiStub,
	                    func=guiStub.myFunc,
	                    endFunc=guiStub.myEndFunc,
	                    funcArgs={'name': 'Jean-Pierre', 'age': 61},
	                    endFuncArgs=('paulo le scientifique', 14))
	
	ste.start()
	time.sleep(6)

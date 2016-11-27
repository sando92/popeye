class Criteria():
	def __init__(self, name=None, args=None): #name string, args list of string
		self.name = name
		self.args = args

	def getName(self):
		return self.name

	def getArgs(self):
		return self.args

class Criteria():
	def __init__(self, name=None, args=None): #name string, args list of string
		self.name = name
		self.args = args

	def set_name(self, name):
		self.name = name

	def set_args(self, args):
		self.args = args

	def get_name(self):
		return self.name

	def get_args(self):
		return self.args

import re

class Proxy:
	def __init__(self):
		self.ip = None
		self.port = None
		self.user = None
		self.password = None

	def getIp(self):
		return self.ip
	def getPort(self):
		return self.port
	def getUser(self):
		return self.user
	def getPassword(self):
		return self.password

	def setIp(self, ip: str):
		if re.fullmatch('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip) == None:
			raise Exception("Proxy must be valid!")
		else:
			self.ip = ip
	def setPort(self, port: int):
		if port in range(0, 65535):
			self.port = port
		else:
			raise Exception("Proxy's port must be between 0 and 65535!")
	def setUser(self, username: str):
		if username == "" or username ==None:
			raise Exception("Proxy user must be specified!")
		else:
			self.user = username
	def setPassword(self, password: str):
		if password == "" or password == None:
			raise Exception("Proxy password must be specified!")
		else:
			self.password = password
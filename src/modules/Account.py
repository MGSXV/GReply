from init.packages import re

class Account:
	def __init__(self):
		self.email = ""
		self.password = ""
		self.proxyIp = "0.0.0.0"
		self.proxyPort = -1
		self.proxyUser = ""
		self.proxyPassword = ""

	# Getters
	def getEmail(self):
		return self.email
	def getPassword(self):
		return self.password
	def getProxyIp(self):
		return self.proxyIp
	def getProxyPort(self):
		return self.proxyPort
	def getProxyUser(self):
		return self.proxyUser
	def getProxyPassword(self):
		return self.proxyPassword

	# Setters
	def setEmail(self, email):
		if re.fullmatch("[a-zA-Z0-9]{2,50}[\-|_|\.]*[a-zA-Z0-9]{2,50}@yahoo{1}(\.[a-zA-Z]{2,4}){1,2}", email) == None:
			raise Exception("All emails should be valid!")
		else:
			self.email = email
	def setPassword(self, password):
		if password == "" or password == None:
			raise Exception("Email password is empty!")
		else:
			self.password = password
	def setProxyIp(self, proxyIp):
		if re.fullmatch('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', proxyIp) == None:
			raise Exception("Proxy must be valid!")
		else:
			self.proxyIp = proxyIp
	def setProxyPort(self, port: int):
		if port in range(0, 65535):
			self.proxyPort = port
		else:
			raise Exception("Proxy's port must be between 0 and 65535!")
	def setProxyUser(self, username):
		if username == "" or username ==None:
			raise Exception("Proxy user must be specified!")
		else:
			self.proxyUser = username
	def setProxyPassword(self, password):
		if password == "" or password == None:
			raise Exception("Proxy password must be specified!")
		else:
			self.proxyPassword = password
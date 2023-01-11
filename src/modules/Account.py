import re

class Account:
	def __init__(self):
		self.email = ""
		self.password = ""
		self.account_info = None
		self.email_index = 1
		self.total_emails = 1
		self.is_active = False
		self.tab_index = -1

	# Getters
	def getEmail(self):
		return self.email
	def getPassword(self):
		return self.password

	# Setters
	def setEmail(self, email):
		if re.fullmatch("[a-zA-Z0-9]{2,50}[\-|_|\.]*[a-zA-Z0-9]{2,50}@gmail{1}(\.com){1}", email) == None:
			raise Exception("All emails should be valid!")
		else:
			self.email = email
	def setPassword(self, password):
		if password == "" or password == None:
			raise Exception("Email password is empty!")
		else:
			self.password = password
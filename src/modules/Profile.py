from modules.Proxy import Proxy
from modules.Account import Account

class Profile:
	def __init__(self):
		self.name = None
		self.accounts = []
		self.proxy = Proxy()

	def getName(self) -> str:
		return self.name
	def getProxy(self) -> Proxy:
		return self.proxy
	def getAccounts(self) -> list:
		return self.accounts

	def setName(self, name:str):
		if name == "" or name is None:
			raise Exception("Profile name is empty!")
		self.name = name
	def setProxy(self, proxy:Proxy):
		self.proxy = proxy
	def setAccounts(self, accounts:list):
		self.accounts = accounts
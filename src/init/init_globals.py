import os

class PATHS:
	SEP = os.path.sep
	CWD = os.getcwd()
	ASSETS = 'assets'
	STORAGE = 'storage'
	LOG_FILE = CWD + SEP + STORAGE + SEP + 'logs'
	CHROME_DRIVER = CWD + SEP + ASSETS + SEP + 'chromedriver.exe'

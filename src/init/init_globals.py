import os

class PATHS:
	SEP = os.path.sep
	CWD = os.getcwd()
	ASSETS = 'assets'
	STORAGE = 'storage'
	LOG_FILE = CWD + SEP + STORAGE + SEP + 'logs'
	CHROME_DRIVER = CWD + SEP + ASSETS + SEP + 'chromedriver.exe'
	RESOURCES_FILE = CWD + SEP + ASSETS + SEP + 'resources.csv'

class ERRORS:
	UNKNOWN_ERROR = -1
	EMAIL_ERROR = 1
	PASS_ERROR = 2
	PROXY_ERROR = 3
	CAPTCHA_ERROR = 4
	BLOCKED_ACC_ERROR = 5
	VERIFICATION_ERROR = 6
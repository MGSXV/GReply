import os
from colored import fg, attr

class PATHS:
	SEP = os.path.sep
	CWD = os.getcwd()
	ASSETS = 'assets'
	STORAGE = 'storage'
	WEBDRIVER_DIR = ASSETS + SEP + 'webdriver'
	PROXY_TEMPLATE_DIR = ASSETS + SEP + 'proxy_template'
	LOG_FILE = CWD + SEP + STORAGE + SEP + 'logs'
	CHROME_DRIVER = CWD + SEP + WEBDRIVER_DIR + SEP + 'chromedriver.exe'
	RESOURCES_FILE = CWD + SEP + ASSETS + SEP + 'accounts.csv'
	MANIFEST_TEMPLATE_FILE = CWD + SEP + PROXY_TEMPLATE_DIR + SEP + 'manifest.json'
	SCRIPT_TEMPLATE_FILE = CWD + SEP + PROXY_TEMPLATE_DIR + SEP + 'background.js'
	CREATIVE = os.getcwd() + SEP + ASSETS + SEP + 'template.html'
	USERNAME= os.getenv('username')
	CHROME_SYS_PATH = f'C:\\Users\\{USERNAME}\\AppData\\Local\\Google\\Chrome\\User Data'

class COLORS:
	DEFAULT = attr("reset")
	BOLD = attr("bold")
	BLACK = fg(0)
	WHITE = fg(255)
	GREY = fg(8)
	RED = fg(1)
	GREEN = fg(82)
	YELLOW = fg(226)
	DODGER_BLUE_2 = fg(27)

	def success_messgae(message: str):
		print(COLORS.GREEN + message + COLORS.DEFAULT)

	def error_messgae(message: str):
		print(COLORS.RED + message + COLORS.DEFAULT)

class ACTIONS:
	ERROR = -1
	HELP = 0
	FILTER = 1
	CONFIG = 2
	SEND = 4
	LOGIN = 5
class ERRORS:
	UNKNOWN_ERROR = -1
	EMAIL_ERROR = 1
	PASS_ERROR = 2
	PROXY_ERROR = 3
	CAPTCHA_ERROR = 4
	BLOCKED_ACC_ERROR = 5
	VERIFICATION_ERROR = 6
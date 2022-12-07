from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from init.init_globals import PATHS, COLORS
from modules.Account import Account
from helpers import file_hanlder

def generate_proxy_extension(account: Account):
	sub_dir = PATHS.STORAGE + PATHS.SEP + account.getEmail().split('@')[0]
	file_hanlder.create_dir_if_not_exist(sub_dir)
	sub_dir = PATHS.STORAGE + PATHS.SEP + account.getEmail().split('@')[0] + PATHS.SEP + 'proxy_extension'
	file_hanlder.create_dir_if_not_exist(sub_dir)
	try:
		manifest_content = file_hanlder.read_file_content(PATHS.MANIFEST_TEMPLATE_FILE)
		script_content = file_hanlder.read_file_content(PATHS.SCRIPT_TEMPLATE_FILE) % {
			"host": account.getProxyIp(),
            "port": account.getProxyPort(),
            "user": account.getProxyUser(),
            "pass": account.getProxyPassword(),
		}
		if not file_hanlder.write_file(sub_dir + PATHS.SEP + 'manifest.json', manifest_content, 'w'):
			return None
		if not file_hanlder.write_file(sub_dir + PATHS.SEP + 'background.js', script_content, 'w'):
			return None
		return sub_dir
	except Exception as e:
		print(e)
		exit(1)

def init_webdriver(account: Account) -> Chrome:
	chrome_options = Options()
	chrome_options.add_argument("--lang={}".format("en"))
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-infobars')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--no-first-run')
	chrome_options.add_argument('--no-service-autorun')
	chrome_options.add_argument('--password-store=basic')
	chrome_options.add_experimental_option("useAutomationExtension", False)
	chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
	chrome_options.add_experimental_option("detach", True)
	chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
	if account.getProxyIp() != '0.0.0.0' or account.getProxyPort() != -1:
		extention = generate_proxy_extension(account)
		if extention is None:
			print('Error while initializing webdriver!')
			return None
		chrome_options.add_argument(f'--load-extension={PATHS.CWD + PATHS.SEP + extention}')
	chrome_dirver = Chrome(chrome_options=chrome_options, executable_path=PATHS.CHROME_DRIVER)
	COLORS.success_messgae('Initializing webdriver is done!')
	return chrome_dirver
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from fake_useragent import UserAgent
from init.init_globals import PATHS, COLORS
import undetected_chromedriver as uc
from modules.Account import Account
from modules.Profile import Profile
from helpers import file_hanlder

def generate_proxy_extension(profile: Profile):
	sub_dir = PATHS.STORAGE + PATHS.SEP + profile.getName()
	file_hanlder.create_dir_if_not_exist(sub_dir)
	sub_dir = PATHS.STORAGE + PATHS.SEP + profile.getName() + PATHS.SEP + 'proxy_extension'
	file_hanlder.create_dir_if_not_exist(sub_dir)
	try:
		manifest_content = file_hanlder.read_file_content(PATHS.MANIFEST_TEMPLATE_FILE)
		script_content = file_hanlder.read_file_content(PATHS.SCRIPT_TEMPLATE_FILE) % {
			"host": profile.proxy.getIp(),
            "port": profile.proxy.getPort(),
            "user": profile.proxy.getUser(),
            "pass": profile.proxy.getPassword(),
		}
		if not file_hanlder.write_file(sub_dir + PATHS.SEP + 'manifest.json', manifest_content, 'w'):
			return None
		if not file_hanlder.write_file(sub_dir + PATHS.SEP + 'background.js', script_content, 'w'):
			return None
		return sub_dir
	except Exception as e:
		print(e)
		exit(1)

def init_webdriver(profile: Profile, config) -> Chrome:
	ua = UserAgent()
	sub_dir = profile.getName()
	userAgent = ua.random
	chrome_options = ChromeOptions()
	chrome_options.add_argument("--lang=en-US")
	chrome_options.add_argument("--disable-popup-blocking")
	chrome_options.add_argument('--disable-blink-features=AutomationControlled')
	# chrome_options.add_experimental_option('prefs', {'int`l.accept_languages': 'en,en_US'})
	# chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
	# chrome_options.add_experimental_option("useAutomationExtension", False)
	chrome_options.set_capability('dom.webdriver.enabled', False)
	chrome_options.add_argument(f'--user-data-dir={PATHS.CHROME_SYS_PATH}')
	chrome_options.add_argument(f'--profile-directory={sub_dir}')
	# chrome_options.binary_location = r'C:\Program Files\SRWare Iron (64-Bit)\chrome.exe'
	if config['proxy']:
		if profile.proxy.getIp() != '0.0.0.0' or profile.proxy.getPort() != -1:
			extention = generate_proxy_extension(profile)
			if extention is None:
				print('Error while initializing webdriver!')
				return None
		chrome_options.add_argument(f'--load-extension={PATHS.CWD + PATHS.SEP + extention}')
	try:
		chrome_dirver = uc.Chrome(options=chrome_options, executable_path=PATHS.CHROME_DRIVER)
		return chrome_dirver
	except Exception as e:
		print(e)
		print(f'{COLORS.RED}Unkown error!{COLORS.DEFAULT}')
		exit(1)
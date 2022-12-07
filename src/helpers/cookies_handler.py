import json
from selenium.webdriver import Chrome
from helpers import file_hanlder
from init.init_globals import PATHS

def save_cookies(path: str, browser: Chrome) -> bool:
	return file_hanlder.write_file(path + PATHS.SEP + 'cookies.json', json.dumps(browser.get_cookies()), 'w')

def load_cookies(path: str, browser: Chrome) -> bool:
	cookies = []
	cookies_file = ''
	try:
		cookies_file = file_hanlder.read_file_content(path + PATHS.SEP + 'cookies.json')
	except:
		return False
	try:
		cookies += json.loads(cookies_file)
	except:
		print('Cookies file error!')
	for cookie in cookies:
		try:
			browser.add_cookie(cookie)
		except:
			pass
	browser.refresh()
	return True
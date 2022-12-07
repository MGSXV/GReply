from helpers import file_hanlder, cookies_handler
from init import init_accounts, init_webdriver
from init.init_globals import PATHS, ACTIONS
from modules.Account import Account
from app import account_handler
import json

def route(account: Account, action: int, config):
	browser = init_webdriver.init_webdriver(account)
	acc_subdir = account.getEmail().split('@')[0]
	if browser is None:
		return 
	browser.get("https://www.google.com")
	cookies_handler.load_cookies(PATHS.STORAGE + PATHS.SEP + acc_subdir, browser)
	if account_handler.is_logged_in(account.getEmail(), browser, config['timeout']):
		pass
	else:
		account_handler.login(account.getEmail(), account.getPassword(), browser, config['timeout'])
	browser.get('https://gmail.com/')
	if action == ACTIONS.CONFIG:
		print('config...')
	elif action == ACTIONS.FILTER:
		print('filter...')
	elif action == ACTIONS.SEND:
		print('send...')
	elif action == ACTIONS.CONFIG + ACTIONS.FILTER:
		print('config filter...')
	else:
		print('unknown action')
		return
	cookies_handler.save_cookies(PATHS.STORAGE + PATHS.SEP + acc_subdir, browser)
	browser.quit()

def entry_point(action: int):
	accs = init_accounts.set_accounts_list()
	config_file = file_hanlder.read_file_content(PATHS.ASSETS + PATHS.SEP + 'config.json')
	config = json.loads(config_file)
	route(accs[0], action, config)
	pass
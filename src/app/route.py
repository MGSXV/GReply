from helpers import file_hanlder, cookies_handler, browser_handler
from init import init_accounts, init_webdriver
from init.init_globals import PATHS, ACTIONS
from modules.Account import Account
from app import account_handler, account_config_handler, account_filter_handler, send_handler
import json
import time
import threading

def route(account: Account, action: int, config):
	browser = init_webdriver.init_webdriver(account, config)
	if browser is None:
		return
	acc_subdir = account.getEmail().split('@')[0]
	if action == ACTIONS.LOGIN:
		if account_handler.login(account.getEmail(), account.getPassword(), account.getRecovery(), browser, config['timeout']):
			cookies_handler.save_cookies(PATHS.STORAGE + PATHS.SEP + acc_subdir, browser)
		return
	browser.get('https://accounts.google.com/')
	browser_handler.wait_time_in_range(2.0, 4.5)
	cookies_handler.load_cookies(PATHS.STORAGE + PATHS.SEP + acc_subdir, browser)
	browser_handler.wait_time_in_range(2.0, 4.5)
	browser.get('https://mail.google.com/')
	if account_handler.is_logged_in(account.getEmail(), browser, config['timeout']):
		if action == ACTIONS.CONFIG:
			account_config_handler.general_settings(browser, config['timeout'])
			account_config_handler.account_settings(browser, config['timeout'], config['config']['from_alias'])
		elif action == ACTIONS.FILTER:
			account_filter_handler.filter_handler(browser, config['timeout'], config['filter']['accept_from_name'])
		elif action == ACTIONS.SEND:
			send_handler.send_proccess(browser, config['timeout'], config['filter']['accept_from_name'], account.getEmail(), config['send'])
		elif action == ACTIONS.CONFIG + ACTIONS.FILTER:
			account_config_handler.general_settings(browser, config['timeout'])
			account_config_handler.account_settings(browser, config['timeout'], config['config']['from_alias'])
			account_filter_handler.filter_handler(browser, config['timeout'], config['filter']['accept_from_name'])
		else:
			print('unknown action')
			return
		cookies_handler.save_cookies(PATHS.STORAGE + PATHS.SEP + acc_subdir, browser)
	browser.quit()

def entry_point(action: int):
	accs = init_accounts.set_accounts_list()
	config_file = file_hanlder.read_file_content(PATHS.ASSETS + PATHS.SEP + 'config.json')
	config = json.loads(config_file)
	# for acc in accs:
	# 	route(acc, action, config)
	route(accs[0], action, config)
	return
	threads_num = config['number_of_threads']
	accounts_num = len(accs)
	threads = []
	i = 0
	thread_handler()
	while (i < accounts_num):
		for j in range(threads_num):
			if i >= accounts_num:
				break
			t = threading.Thread(target=route, args=(accs[i], action, config))
			t.start()
			threads.append(t)
			i+= 1
		time.sleep(1)
		for tt in threads:
			tt.join()
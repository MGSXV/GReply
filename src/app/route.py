from helpers import file_hanlder
from init import init_webdriver, init_profile
from init.init_globals import PATHS, ACTIONS
from modules.Profile import Profile
from app import account_handler, account_config_handler, account_filter_handler, send_handler
import json
import time
import threading

# def route(profile: Profile, action: int, config):
# 	browser = init_webdriver.init_webdriver(profile, config)
# 	if browser is None:
# 		return
# 	# acc_subdir = account.getEmail().split('@')[0]
# 	if action == ACTIONS.LOGIN:
# 		print('login...')
# 		# if account_handler.login(account.getEmail(), account.getPassword(), browser, config['timeout']):
# 		# 	cookies_handler.save_cookies(PATHS.STORAGE + PATHS.SEP + acc_subdir, browser)
# 		return
# 	# browser.get('https://accounts.google.com/')
# 	# browser_handler.wait_time_in_range(2.0, 4.5)
# 	# cookies_handler.load_cookies(PATHS.STORAGE + PATHS.SEP + acc_subdir, browser)
# 	# browser_handler.wait_time_in_range(2.0, 4.5)
# 	# browser.get('https://mail.google.com/')
# 	if account_handler.is_logged_in(account.getEmail(), browser, config['timeout']):
# 		if action == ACTIONS.CONFIG:
# 			account_config_handler.general_settings(browser, config['timeout'])
# 			account_config_handler.account_settings(browser, config['timeout'], config['config']['from_alias'])
# 		elif action == ACTIONS.FILTER:
# 			account_filter_handler.filter_handler(browser, config['timeout'], config['filter']['accept_from_name'])
# 		elif action == ACTIONS.SEND:
# 			send_handler.send_proccess(browser, config['timeout'], config['filter']['accept_from_name'], account.getEmail(), config['send'])
# 		elif action == ACTIONS.CONFIG + ACTIONS.FILTER:
# 			account_config_handler.general_settings(browser, config['timeout'])
# 			account_config_handler.account_settings(browser, config['timeout'], config['config']['from_alias'])
# 			account_filter_handler.filter_handler(browser, config['timeout'], config['filter']['accept_from_name'])
# 		else:
# 			print('unknown action')
# 			return
# 		cookies_handler.save_cookies(PATHS.STORAGE + PATHS.SEP + acc_subdir, browser)
# 	browser.quit()

def route(profile: Profile, action: int, config):
	browser = init_webdriver.init_webdriver(profile, config)
	if browser is None:
		return
	if action == ACTIONS.LOGIN:
		account_handler.account_group(profile.accounts, browser, config['timeout'])
	elif action == ACTIONS.CONFIG:
		print('config...')
	elif action == ACTIONS.FILTER:
		print('filter...')
	elif action == ACTIONS.SEND:
		print('send...')
	elif action == ACTIONS.CONFIG + ACTIONS.FILTER:
		print('filter / config...')
	else:
		print('unknown action')
	browser.quit()

def entry_point(action: int):
	# accs = init_accounts.set_accounts_list()
	profiles = init_profile.set_profiles_list()
	config_file = file_hanlder.read_file_content(PATHS.ASSETS + PATHS.SEP + 'config.json')
	config = json.loads(config_file)
	for profile in profiles:
		route(profile, action, config)
	# route(profiles[0], action, config)
	return
	# number_of_threads = config['number_of_threads']
	# acc_per_browser = config['accounts_per_browser']
	# number_of_accs = len(accs)
	# if acc_per_browser < 1:
	# 	acc_per_browser = 1
	# elif acc_per_browser > number_of_accs:
	# 	acc_per_browser = number_of_accs
	# threads = []
	# i = 0
	# while (i < number_of_accs):
	# 	for j in range(number_of_threads):
	# 		if i >= number_of_accs:
	# 			break
	# 		limit = acc_per_browser + i
	# 		if limit > number_of_accs:
	# 			limit = number_of_accs
	# 		t = threading.Thread(target=route, args=(accs[i:limit], action, config))
	# 		t.start()
	# 		threads.append(t)
	# 		i+= acc_per_browser
	# 	time.sleep(1)
	# 	for tt in threads:
	# 		tt.join()
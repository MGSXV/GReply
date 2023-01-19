from helpers import file_hanlder
from init import init_webdriver, init_profile
from init.init_globals import PATHS, ACTIONS
from modules.Profile import Profile
from app import account_handler, account_config_handler, account_filter_handler, send_handler, account_alias_handler
import json

def route(profile: Profile, action: int, config):
	browser = init_webdriver.init_webdriver(profile, config)
	if browser is None:
		return
	if action == ACTIONS.LOGIN:
		account_handler.account_group(profile.accounts, browser, config['timeout'])
	elif action == ACTIONS.CONFIG:
		account_config_handler.accounts_group_config(profile.accounts, browser, config['timeout'], config['config']['from_alias'])
	elif action == ACTIONS.FILTER:
		account_filter_handler.accounts_group_filter(profile.accounts, browser, config['timeout'], config['filter']['accept_from_name'])
	elif action == ACTIONS.SEND:
		send_handler.send_group_send(profile.accounts, browser, config['timeout'], config['filter']['accept_from_name'], config)
	elif action == ACTIONS.CONFIG + ACTIONS.FILTER:
		account_filter_handler.accounts_group_filter_config(profile.accounts, browser, config['timeout'], config['filter']['accept_from_name'], config['config']['from_alias'])
	elif action == ACTIONS.ALIAS:
		account_alias_handler.alias_group_handler(profile.accounts, browser, config)
	elif action == ACTIONS.BOUNCE:
		print("bounce...")
	else:
		print('unknown action')
	browser.close()
	browser.quit()

def entry_point(action: int):
	file_hanlder.create_dir_if_not_exist(PATHS.STORAGE)
	profiles = init_profile.set_profiles_list()
	config_file = file_hanlder.read_file_content(PATHS.ASSETS + PATHS.SEP + 'config.json')
	config = json.loads(config_file)
	for profile in profiles:
		route(profile, action, config)
	# route(profiles[0], action, config)
	return
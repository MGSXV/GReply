from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from helpers import browser_handler
import random

def open_all_accounts(accounts: list, browser: Chrome):
	i = 0
	for acc in accounts:
		old_url = f'https://mail.google.com/mail/u/{i}/#settings/accounts'
		browser.get(old_url)
		browser_handler.wait_time_in_range(1.5, 3.5)
		new_url = browser.current_url
		if new_url != old_url:
			browser.execute_script("window.close('','_parent','');")
			browser.switch_to.window(browser.window_handles[0])
			break
		browser.execute_script('''window.open("about:blank");''')
		i = i + 1
		browser.switch_to.window(browser.window_handles[i])

def get_active_accounts(accounts: list, browser: Chrome) -> list:
	num_of_tabs = len(browser.window_handles)
	accs = []
	for i in range(num_of_tabs):
		browser.switch_to.window(browser.window_handles[i])
		for account in accounts:
			if account.email.lower() in browser.title:
				account.is_active = True
				account.tab_index = i
				accs.append(account)
	return accs

def get_randomized_alias(email: str, alias_sufix: str) -> str:
	mail_alias = email.split('@')[0]
	domain = email.split('@')[1]
	alias_len = len(mail_alias)
	new_alias = ''
	for i in range(alias_len):
		if mail_alias[i] != '.':
			new_alias += mail_alias[i]
		if random.getrandbits(1) and mail_alias[i] != '.' and new_alias[-1] != '.':
			new_alias += '.'
	new_alias = new_alias.rstrip('.')
	for i in range(random.randint(1, 10)):
		new_alias += '+'
	new_alias += alias_sufix + '@' + domain
	return new_alias

def handle_new_window(browser: Chrome, timeout: int, from_alias: str, new_alias: str):
	tabs_num = len(browser.window_handles) - 1
	browser.switch_to.window(browser.window_handles[tabs_num])
	xpath = '/html/body/div/table/tbody/tr[2]/td/table/tbody/tr[3]/td/form/table/tbody/tr[1]/td[2]/input'
	browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
	element = browser.find_element(By.XPATH, xpath)
	element.clear()
	browser_handler.simulate_human_typing(from_alias, element)
	browser_handler.wait_time_in_range(1.2, 1.7)
	xpath = '/html/body/div/table/tbody/tr[2]/td/table/tbody/tr[3]/td/form/table/tbody/tr[2]/td[2]/input'
	browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
	element = browser.find_element(By.XPATH, xpath)
	element.clear()
	browser_handler.simulate_human_typing(new_alias, element)
	browser_handler.wait_time_in_range(1.2, 1.7)
	xpath = '/html/body/div/table/tbody/tr[2]/td/table/tbody/tr[3]/td/form/table/tbody/tr[7]/td/input[3]'
	browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
	element = browser.find_element(By.XPATH, xpath)
	element.click()
	


def add_new_alias(browser: Chrome, timeout: int, index: int, from_alias: str, new_alias: str):
	xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[4]/div/table/tbody/tr[4]/td[2]/table[1]/tbody/tr[2]/td[1]/span'
	browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
	element = browser.find_element(By.XPATH, xpath)
	element.click()
	handle_new_window(browser, timeout, from_alias, new_alias)
	browser.switch_to.window(browser.window_handles[index])
	xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[4]/div/table/tbody/tr[4]/td[2]/table[1]/tbody/tr[2]/td[2]/span'
	browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
	element = browser.find_element(By.XPATH, xpath)
	if element.text == 'make default':
		element.click()


def delete_confirmation_handler(browser: Chrome, index: int):
	try:
		xpath = f'/html/body/div[{index}]/div[3]/button[1]'
		element = browser.find_element(By.XPATH, xpath)
		element.click()
	except:
		browser_handler.wait_time_in_range(3.0, 5.0)
		delete_confirmation_handler(browser, index + 1)


def delete_old_alias(browser: Chrome, timeout: int):
	xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[4]/div/table/tbody/tr[4]/td[2]/table[1]/tbody/tr[2]/td[4]/span'
	browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
	element = browser.find_element(By.XPATH, xpath)
	element.click()
	browser_handler.wait_time_in_range(1.2, 1.5)
	delete_confirmation_handler(browser, 18)


def set_new_email_alias(browser: Chrome, timeout: int, index: int, from_alias: str, new_alias: str):
	try:
		xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[4]/div/table/tbody/tr[4]/td[2]/table[1]'
		browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
		subtable = browser.find_element(By.XPATH, xpath)
		xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[4]/div/table/tbody/tr[4]/td[2]/table[1]/tbody/tr[2]'
		browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
		element = subtable.find_element(By.XPATH, xpath)
		if element.text == 'Add another email address':
			add_new_alias(browser, timeout, index, from_alias, new_alias)
		else:
			delete_old_alias(browser, timeout)
			add_new_alias(browser, timeout, index, from_alias, new_alias)
	except Exception as e:
		print(e)

def alias_group_handler(accounts:list, browser: Chrome, config):
	open_all_accounts(accounts, browser)
	acc_list = get_active_accounts(accounts, browser)
	for acc in acc_list:
		browser.switch_to.window(browser.window_handles[acc.tab_index])
		new_alias = get_randomized_alias(acc.email, config['config']['alias_suffix'])
		set_new_email_alias(browser, config['timeout'], acc.tab_index, config['config']['from_alias'], new_alias)
	import time
	time.sleep(100000)
		# print(acc.email, get_randomized_alias(acc.email, config['config']['alias_suffix']))

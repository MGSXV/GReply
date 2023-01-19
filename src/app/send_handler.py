from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from modules.Account import Account
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from helpers import browser_handler
from init.init_globals import PATHS, ERRORS
from helpers.logs_handler import Logger

def locate_email(browser: Chrome, timeout: int, accepted_from: str, xpath: str) -> WebElement or None:
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
		element = browser.find_element(By.XPATH, xpath)
		subj_xpath = xpath.rstrip('td[4]') + '/td[5]/div/div'
		if accepted_from.lower() in element.text.lower():
			element = browser.find_element(By.XPATH, subj_xpath)
			return element
		return None
	except Exception as e:
		return None

def get_creative(browser: Chrome, timeout: int, index: int):
	action = ActionChains(browser)
	xpath ='/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[2]/div/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div/div[2]/div[3]/div/table/tbody/tr/td[2]/div[2]/div/div[1]'
	browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
	element = browser.find_element(By.XPATH, xpath)
	browser.switch_to.window(browser.window_handles[0])
	browser.refresh()
	browser_handler.wait_time_in_range(0.7, 1.0)
	action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
	browser_handler.wait_time_in_range(0.2, 0.5)
	action.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
	browser.switch_to.window(browser.window_handles[index])
	element.click()
	browser_handler.wait_time_in_range(0.5, 0.9)
	action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
	browser_handler.wait_time_in_range(0.5, 0.9)
	ActionChains(browser).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()

def send_reply(browser: Chrome, timeout: int, index: int):
	xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[4]/div[1]'
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
		element = browser.find_element(By.XPATH, xpath)
		element.click()
		browser_handler.wait_time_in_range(1.1, 1.5)
		get_creative(browser, timeout, index)
	except Exception as e:
		print(e)

def back_to_inbox(browser: Chrome, timeout: int):
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div/div[1]/div')
		element = browser.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div/div[1]/div')
		element.click()
	except:
		browser.get('https://mail.google.com/mail/u/0/#inbox')

def open_all_accounts(accounts: list, browser: Chrome, accepted_from: str):
	i = 1
	for acc in accounts:
		browser.execute_script('''window.open("about:blank");''')
		browser.switch_to.window(browser.window_handles[i])
		_from = accepted_from.replace(' ', '+')
		old_url = f'https://mail.google.com/mail/u/{i - 1}/#search/is%3Aunread+from%3A({_from})'
		browser.get(old_url)
		browser_handler.wait_time_in_range(1.5, 3.5)
		new_url = browser.current_url
		if new_url != old_url:
			browser.execute_script("window.close('','_parent','');")
			browser.switch_to.window(browser.window_handles[0])
			break
		i = i + 1
	return i - 1

def get_active_accounts(accounts: list, browser: Chrome, timeout: int) -> list:
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

def send_group_send(accounts: list, browser: Chrome, timeout: int, accepted_from: str, config):
	browser.get(PATHS.CREATIVE)
	num_of_accs = open_all_accounts(accounts, browser, accepted_from)
	accs_list = get_active_accounts(accounts, browser, timeout)
	tbody_xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[5]/div[1]/div/table/tbody'
	browser.switch_to.window(browser.window_handles[accs_list[0].tab_index])
	while num_of_accs != 0:
		for acc in accs_list:
			browser.switch_to.window(browser.window_handles[acc.tab_index])
			element = locate_email(browser, timeout, accepted_from, f'{tbody_xpath}/tr[{acc.email_index}]/td[4]')
			if element is not None:
				element.click()
				browser_handler.wait_time_in_range(1.4, 2.5)
				send_reply(browser, timeout, acc.tab_index)
				browser_handler.wait_time_in_range(1.4, 1.5)
				back_to_inbox(browser, timeout)
			else:
				browser.execute_script("window.close('','_parent','');")
				accs_list = get_active_accounts(accounts, browser, timeout)
				num_of_accs = num_of_accs - 1
				break
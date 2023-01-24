from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from modules.Account import Account
from helpers.logs_handler import Logger
from helpers import browser_handler, cookies_handler
from init.init_globals import PATHS, ERRORS, COLORS
import time

def is_logged_in(email: str, browser: Chrome, timeout: int) -> bool:
	xpath = '/html/body/div[7]/div[3]/div/div[1]/div[3]/header/div[2]/div[3]/div[1]/div[2]/div/a'
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
		element = browser.find_element(By.XPATH, xpath)
		aria_label = element.get_attribute('aria-label')
		if email in aria_label:
			return True
		return False
	except:
		return False

# def requires_verification(browser: Chrome, timeout: int, verif) -> int:
# 	try:
# 		browser_handler.wait_for_element_by_id(browser, timeout, 'view_container')
# 		while True:
# 			browser_handler.wait_time_in_range(2.5, 3.5)
# 			element = browser.find_element(By.ID, 'view_container')
# 			if element.text != verif:
# 				break
# 		# print(element.text)
# 		if 'Confirm your recovery email' in element.text:
# 			print('Confirm your recovery email')
# 			return 1
# 		elif 'Your account has been disabled' in element.text:
# 			print('Your account has been disabled')
# 			return ERRORS.BLOCKED_ACC_ERROR
# 		elif 'Confirm your recovery phone number' in element.text:
# 			print('Confirm your recovery phone number')
# 			return 0
# 		elif 'Verify that it’s you' in element.text:
# 			print('Verify that it’s you')
# 			return ERRORS.VERIFICATION_ERROR
# 	except:
# 		return -1

def login(email: str, password: str, browser: Chrome, timeout: int, index: int) -> bool:
	try:
		browser.get('https://accounts.google.com/signin/chrome/sync/identifier?ssp=1&continue=https%3A%2F%2Fwww.google.com%2F&flowName=GlifDesktopChromeSync&hl=en-GB')
		browser_handler.wait_for_element_by_id(browser, timeout, 'identifierId')
		element = browser.find_element(By.ID, 'identifierId')
		browser_handler.simulate_human_typing(email, element)
		browser_handler.wait_for_element_by_xpath(browser, timeout, '//*[@id="identifierNext"]/div/button')
		element = browser.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button')
		browser_handler.wait_time_in_range(2.5, 3.5)
		element.click()
	except:
		print('Error type email!')
		Logger.logger(ERRORS.EMAIL_ERROR, email, 'error_logs')
		return False
	browser_handler.wait_time_in_range(2.5, 3.5)
	browser_handler.wait_for_element_by_id(browser, timeout, 'view_container')
	verif = browser.find_element(By.ID, 'view_container').text
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, '//*[@id="password"]/div[1]/div/div[1]/input')
		element = browser.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
		browser_handler.simulate_human_typing(password, element)
		browser_handler.wait_for_element_by_xpath(browser, timeout, '//*[@id="passwordNext"]/div/button')
		element = browser.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button')
		browser_handler.wait_time_in_range(1.5, 3.5)
		element.click()
	except:
		print('Error type password!')
		Logger.logger(ERRORS.PASS_ERROR, email, 'error_logs')
		return False
	browser_handler.wait_time_in_range(2.5, 4.5)
	current_url = browser.current_url
	if 'https://www.google.com/' != current_url:
		Logger.logger(ERRORS.VERIFICATION_ERROR, email, 'error_logs')
		return False
	return True
	
def account_group(accounts: list, browser: Chrome, timeout: int):
	accs_num = len(accounts)
	if accs_num == 0:
		return
	i = 0
	for acc in accounts:
		login(acc.getEmail(), acc.getPassword(), browser, timeout, i)
		i = i + 1
		if i < accs_num:
			browser.execute_script('''window.open("about:blank");''')
			browser.switch_to.window(browser.window_handles[i])
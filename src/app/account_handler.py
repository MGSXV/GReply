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

def requires_verification(browser: Chrome, timeout: int) -> int:
	css = '#view_container > div > div > div:nth-child(1) > div > div.aCayab > div'
	try:
		browser_handler.wait_for_element_by_css_selector(browser, timeout, css)
		element = browser.find_element(By.ID, 'view_container')
		if 'Confirm your recovery email' in element.text:
			return 1
		elif 'Your account has been disabled' in element.text:
			return ERRORS.BLOCKED_ACC_ERROR
		elif 'Confirm your recovery phone number' in element.text:
			return 0
	except:
		return -1

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
		return False
	browser_handler.wait_time_in_range(2.5, 3.5)
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
		return False
	res = requires_verification(browser, timeout)
	if res == 1:
		Logger.logger(ERRORS.VERIFICATION_ERROR, email)
		return False
		pass #TODO: USe verifcation email
	elif res == 0:
		Logger.logger(Logger.VERIFICATION_ERROR, email)
		return False
	elif res == ERRORS.BLOCKED_ACC_ERROR:
		Logger.logger(res, email)
		return False
	elif res == -1:
		Logger.logger(ERRORS.VERIFICATION_ERROR, email)
		return False
	browser_handler.wait_time_in_range(2.5, 4.5)
	browser.get(f'https://mail.google.com/mail/u/{index}/#inbox')
	res =  is_logged_in(email, browser, timeout)
	if res:
		browser_handler.wait_time_in_range(2.5, 4.5)
		cookies_handler.save_cookies(PATHS.STORAGE + PATHS.SEP + email.split('@')[0], browser)
		browser.get(f'https://myaccount.google.com/u/{index}/')
		browser_handler.wait_time_in_range(2.5, 4.5)
		cookies_handler.save_cookies(PATHS.STORAGE + PATHS.SEP + email.split('@')[0], browser)
		return True
	Logger.logger(ERRORS.VERIFICATION_ERROR, email)
	return False
	
def account_group(accounts: list, browser: Chrome, timeout: int):
	accs_num = len(accounts)
	if accs_num == 0:
		return
	i = 0
	for acc in accounts:
		login(acc.getEmail(), acc.getPassword(), browser, timeout)
		i = i + 1
		if i < accs_num:
			browser.execute_script('''window.open("about:blank");''')
			browser.switch_to.window(browser.window_handles[i])
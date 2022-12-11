from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from helpers.logs_handler import Logger
from helpers import browser_handler, cookies_handler
from init.init_globals import PATHS, ERRORS

def is_logged_in(email: str, browser: Chrome, timeout: int) -> bool:
	xpath = '/html/body/div[1]/div[1]/div/div/div/div[2]/div[2]/div/a'
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
		return 0
	except:
		return -1

def verify_account(browser: Chrome, timeout: int, recovery: str) -> bool:
	if recovery == '' or recovery == None:
		return False
	return True
	

def login(email: str, password: str, recovery: str, browser: Chrome, timeout: int) -> bool:
	browser.get('https://accounts.google.com/v3/signin/identifier?flowName=GlifWebSignIn&hl=en-GB&flowEntry=ServiceLogin')
	try:
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
	vres = requires_verification(browser, timeout)
	if vres == -1:
		return True
	elif vres == 0:
		Logger.logger(ERRORS.VERIFICATION_ERROR, email)
		return False
	elif vres == ERRORS.BLOCKED_ACC_ERROR:
		Logger.logger(ERRORS.BLOCKED_ACC_ERROR, email)
		return False
	else:
		if not verify_account(browser, timeout, recovery):
			return False
	# cookies_handler.save_cookies(PATHS.STORAGE + PATHS.SEP + email.split('@')[0], browser)
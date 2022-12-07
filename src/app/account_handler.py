from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from helpers import browser_handler, cookies_handler
from init.init_globals import PATHS

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

def login(email: str, password: str, browser: Chrome, timeout: int):
	try:
		browser_handler.wait_for_element_by_id(browser, timeout, 'identifierId')
		element = browser.find_element(By.ID, 'identifierId')
		browser_handler.simulate_human_typing(email, element)
		browser_handler.wait_for_element_by_xpath(browser, timeout, '//*[@id="identifierNext"]/div/button')
		browser_handler.wait_time_in_range(1.5, 3,5)
		element = browser.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button')
		element.click()
	except:
		print('Error type email!')
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, '//*[@id="password"]/div[1]/div/div[1]/input')
		element = browser.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
		browser_handler.simulate_human_typing(password, element)
		browser_handler.wait_for_element_by_xpath(browser, timeout, '//*[@id="passwordNext"]/div/button')
		browser_handler.wait_time_in_range(1.5, 3,5)
		browser.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button')
		element.click()
	except:
		pass
	cookies_handler.save_cookies(PATHS.STORAGE + PATHS.SEP + email.split('@')[0], browser)
	pass
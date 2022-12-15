from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from helpers import browser_handler

def filter_actions(browser: Chrome, timeout: int, xpath: str, iswritable: bool, towrite: str):
	browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
	browser_handler.wait_time_in_range(1.0, 1.5)
	element = browser.find_element(By.XPATH, xpath)
	element.click()
	if iswritable:
		element.clear()
		browser_handler.simulate_human_typing(towrite, element)

def filter_options(browser: Chrome, lable_name: str, j:int):
	i = 0
	browser_handler.wait_time_in_range(3.1, 5.3)
	while (i:=i+1):
		xpath = f'/html/body/div[{i}]/div/div[2]/div[3]/div/div[{j}]/label'
		try:
			browser_handler.wait_time_in_range(.1, .3)
			element = browser.find_element(By.XPATH, xpath)
			if lable_name in element.text:
				return xpath
			if i > 30:
				break
		except:
			if i > 30:
				break
			continue
	return ''

def filter_handler(browser: Chrome, timeout: int, accepted_from: str):
	browser.get('https://mail.google.com/mail/u/0/#inbox')
	filter_xpath = '//*[@id="aso_search_form_anchor"]/button[2]'
	try:
		# Filter icon in search
		filter_actions(browser, timeout, filter_xpath, False, '')
		# From name input
		i = 0
		browser_handler.wait_time_in_range(3.1, 5.3)
		while (i:=i+1):
			xpath = f'/html/body/div[{i}]/div/div[2]/div[1]/span[1]/label'
			try:
				browser_handler.wait_time_in_range(.1, .3)
				element = browser.find_element(By.XPATH, xpath)
				if element.text == 'From':
					xpath = f'/html/body/div[{i}]/div/div[2]/div[1]/span[2]/input'
					filter_actions(browser, timeout, xpath, True, accepted_from)
					break
				if i > 30:
					break
			except:
				if i > 30:
					break
				continue
		# Create filter button
		xpath = f'/html/body/div[{i}]/div/div[2]/div[10]/div[2]'
		browser_handler.wait_time_in_range(1.1, 3.3)
		filter_actions(browser, timeout, xpath, False, '')
		# Filter settings
		xpath = filter_options(browser, 'Never send it to Spam', 7)
		if xpath != '':
			filter_actions(browser, timeout, xpath, False, '')
		xpath = filter_options(browser, 'Always mark it as important', 8)
		if xpath != '':
			filter_actions(browser, timeout, xpath, False, '')
		xpath = filter_options(browser, 'Categorize as:', 10)
		if xpath != '':
			xpath = xpath.replace('lable', 'div/div[1]')
			filter_actions(browser, timeout, xpath, False, '')
		browser_handler.wait_time_in_range(200.0, 300.0)
	except Exception as e:
		print(e)
	
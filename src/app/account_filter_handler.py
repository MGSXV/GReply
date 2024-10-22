from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from helpers import browser_handler
from app import account_config_handler as ach

def filter_actions(browser: Chrome, timeout: int, xpath: str, iswritable: bool, towrite: str):
	browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
	browser_handler.wait_time_in_range(1.0, 1.5)
	element = browser.find_element(By.XPATH, xpath)
	element.click()
	if iswritable:
		element.clear()
		browser_handler.simulate_human_typing(towrite, element)

def filter_options(browser: Chrome, lable_name: str, j:int, i: int):
	browser_handler.wait_time_in_range(.7, 1.7)
	xpath = f'/html/body/div[{i}]/div/div[2]/div[3]/div/div[{j}]/label'
	try:
		browser_handler.wait_time_in_range(.1, .3)
		element = browser.find_element(By.XPATH, xpath)
		if lable_name in element.text:
			return [xpath, i]
		else:
			return filter_options(browser, lable_name, j + 1, i)
	except:
		return ['', i]

def bounce_handler(browser: Chrome, timeout: int):
	filter_xpath = '//*[@id="aso_search_form_anchor"]/button[2]'
	try:
		# Filter icon in search
		filter_actions(browser, timeout, filter_xpath, False, '')
		# From name input
		i = 15
		browser_handler.wait_time_in_range(3.1, 5.3)
		while (i:=i+1):
			xpath = f'/html/body/div[{i}]/div/div[2]/div[1]/span[1]/label'
			try:
				browser_handler.wait_time_in_range(.1, .3)
				element = browser.find_element(By.XPATH, xpath)
				if element.text == 'From':
					xpath = f'/html/body/div[{i}]/div/div[2]/div[1]/span[2]/input'
					filter_actions(browser, timeout, xpath, True, 'Mail Delivery Subsystem')
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
		i = i + 1
		xpath = filter_options(browser, 'Categorize as:', 10, i)
		if xpath[0] == '':
			xpath = filter_options(browser, 'Categorise as:', 10, i)
		if xpath[0] != '':
			xpath[0] = xpath[0].replace('label', 'div/div[1]')
			filter_actions(browser, timeout, xpath[0], False, '')
			browser_handler.wait_time_in_range(1.1, 2.2)
			xpath[0] = xpath[0].replace('div/div[1]', 'div[2]/div[3]')
			filter_actions(browser, timeout, xpath[0], False, '')
		xpath[0] = f'/html/body/div[{xpath[1]}]/div/div[2]/div[4]/div'
		browser_handler.wait_for_element_by_xpath(browser, timeout, xpath[0])
		element = browser.find_element(By.XPATH, xpath[0])
		element.click()
		browser_handler.wait_time_in_range(2.0, 3.0)
	except:
		pass

def filter_handler(browser: Chrome, timeout: int, accepted_from: str, index: int):
	old_url = f'https://mail.google.com/mail/u/{index}/#inbox'
	browser.get(old_url)
	filter_xpath = '//*[@id="aso_search_form_anchor"]/button[2]'
	browser_handler.wait_time_in_range(1.0, 1.5)
	new_url = browser.current_url
	if old_url != new_url:
		return
	try:
		# Filter icon in search
		filter_actions(browser, timeout, filter_xpath, False, '')
		# From name input
		i = 15
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
		browser.find_element(By.XPATH, f'/html/body/div[{i}]/div/div[2]/div[1]/span[1]/label').click()
		xpath = f'/html/body/div[{i}]/div/div[2]/div[10]/div[2]'
		browser_handler.wait_time_in_range(1.1, 3.3)
		filter_actions(browser, timeout, xpath, False, '')
		# Filter settings
		i = i + 1
		xpath = filter_options(browser, 'Never send it to Spam', 7, i)
		if xpath[0] != '':
			filter_actions(browser, timeout, xpath[0], False, '')
		xpath = filter_options(browser, 'Always mark it as important', 8, i)
		if xpath[0] != '':
			filter_actions(browser, timeout, xpath[0], False, '')
		xpath = filter_options(browser, 'Categorize as:', 10, i)
		if xpath[0] == '':
			xpath = filter_options(browser, 'Categorise as:', 10, i)
		if xpath[0] != '':
			xpath[0] = xpath[0].replace('label', 'div/div[1]')
			filter_actions(browser, timeout, xpath[0], False, '')
			browser_handler.wait_time_in_range(1.1, 2.2)
			xpath[0] = xpath[0].replace('div/div[1]', 'div[2]/div[2]')
			filter_actions(browser, timeout, xpath[0], False, '')
		xpath[0] = f'/html/body/div[{xpath[1]}]/div/div[2]/div[4]/div'
		browser_handler.wait_for_element_by_xpath(browser, timeout, xpath[0])
		element = browser.find_element(By.XPATH, xpath[0])
		element.click()
		browser_handler.wait_time_in_range(2.0, 3.0)
	except Exception as e:
		print(e)

def accounts_group_filter(accounts:list, browser: Chrome, timeout: int, from_name: str):
	num_of_accs = ach.open_all_accounts(accounts, browser)
	accs_list = ach.get_active_accounts(accounts, browser)
	if num_of_accs == 0:
		return
	for account in accs_list:
		browser.switch_to.window(browser.window_handles[account.tab_index])
		filter_handler(browser, timeout, from_name, account.tab_index)
		bounce_handler(browser, timeout)

def accounts_group_filter_bounce(accounts:list, browser: Chrome, timeout: int):
	num_of_accs = ach.open_all_accounts(accounts, browser)
	accs_list = ach.get_active_accounts(accounts, browser)
	if num_of_accs == 0:
		return
	for account in accs_list:
		browser.switch_to.window(browser.window_handles[account.tab_index])
		bounce_handler(browser, timeout)

def accounts_group_filter_from(accounts:list, browser: Chrome, timeout: int, from_name: str):
	num_of_accs = ach.open_all_accounts(accounts, browser)
	accs_list = ach.get_active_accounts(accounts, browser)
	if num_of_accs == 0:
		return
	for account in accs_list:
		browser.switch_to.window(browser.window_handles[account.tab_index])
		filter_handler(browser, timeout, from_name, account.tab_index)

def accounts_group_filter_config(accounts:list, browser: Chrome, timeout: int, from_name: str, alias_name: str):
	num_of_accs = ach.open_all_accounts(accounts, browser)
	accs_list = ach.get_active_accounts(accounts, browser)
	if num_of_accs == 0:
		return
	for account in accs_list:
		browser.switch_to.window(browser.window_handles[account.tab_index])
		ach.general_settings(browser, timeout, account.tab_index)
		ach.account_settings(browser, timeout, alias_name, account.tab_index, num_of_accs)
		filter_handler(browser, timeout, from_name, account.tab_index)
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from helpers import browser_handler

def lang_handler(browser: Chrome, timeout: int):
	dropdown_xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[1]/div/table/tbody/tr[1]/td[2]/div[1]/select'
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, dropdown_xpath)
		dropdown = Select(browser.find_element(By.XPATH, dropdown_xpath))
		selected = dropdown.first_selected_option
		browser_handler.wait_time_in_range(2.0, 4.0)
		if 'English (US)' != selected.text:
			dropdown.select_by_value('en')
	except:
		pass

def conv_view(browser: Chrome, timeout: int):
	main_div_xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div'
	conv_view_expath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[1]/div/table/tbody/tr[17]/td[1]/span[1]'
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, main_div_xpath)
		main_div = browser.find_element(By.XPATH, main_div_xpath)
		browser_handler.wait_for_element_by_xpath(browser, timeout, conv_view_expath)
		conv_view = browser.find_element(By.XPATH, conv_view_expath)
		conv_view.click()
		browser_handler.wait_time_in_range(2.5, 4.0)
		xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[1]/div/table/tbody/tr[17]/td[2]/table[2]/tbody/tr/td[2]/span/label'
		browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
		element = browser.find_element(By.XPATH, xpath)
		element.click()
		browser_handler.wait_time_in_range(2.5, 4.0)
	except:
		pass

def save_settings(browser: Chrome, timeout: int):
	xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[1]/div/table/tbody/tr[33]/td/div/button[1]'
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
		button = browser.find_element(By.XPATH, xpath)
		browser_handler.wait_time_in_range(2.5, 4.0)
		if not button.get_property('disabled'):
			button.click()
		browser_handler.wait_time_in_range(2.5, 4.0)
	except:
		pass

def general_settings(browser: Chrome, timeout: int, index: int):
	browser.get(f'https://mail.google.com/mail/u/{index}/#settings/general')
	browser_handler.wait_time_in_range(2.0, 4.0)
	lang_handler(browser, timeout)
	browser_handler.wait_time_in_range(2.0, 4.0)
	conv_view(browser, timeout)
	browser_handler.wait_time_in_range(2.0, 4.0)
	save_settings(browser, timeout)

def account_settings(browser: Chrome, timeout: int, from_name: str, index: int):
	browser.get(f'https://mail.google.com/mail/u/{index}/#settings/accounts')
	edit_from_xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[4]/div/table/tbody/tr[4]/td[2]/table/tbody/tr[1]/td[3]/span'
	lable_xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[4]/div/table/tbody/tr[4]/td[1]/span[1]'
	try:
		browser_handler.wait_for_element_to_be_clickable(browser, timeout, lable_xpath)
		browser.find_element(By.XPATH, lable_xpath).click()
		browser_handler.wait_for_element_to_be_clickable(browser, timeout, edit_from_xpath)
		browser_handler.wait_time_in_range(2.0, 4.0)
		edit_from = browser.find_element(By.XPATH, edit_from_xpath)
		browser_handler.wait_time_in_range(2.0, 4.0)
		edit_from.click()
		window_before = browser.window_handles[0 + index]
		browser_handler.wait_time_in_range(0.3, 0.5)
		window_after = browser.window_handles[1 + index]
		browser_handler.wait_time_in_range(0.3, 0.5)
		browser.switch_to.window(window_after)
		from_name_xpath = '/html/body/div/table/tbody/tr[2]/td/table/tbody/tr[3]/td/form/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td[2]/input'
		browser_handler.wait_for_element_by_xpath(browser, timeout, from_name_xpath)
		browser_handler.wait_time_in_range(2.0, 4.0)
		element = browser.find_element(By.XPATH, from_name_xpath)
		browser_handler.simulate_human_typing(from_name, element)
		browser_handler.wait_for_element_by_id(browser, timeout, 'bttn_sub')
		elem = browser.find_element(By.ID, 'bttn_sub')
		elem.click()
		browser.switch_to.window(window_before)
		browser_handler.wait_time_in_range(1.3, 2.5)
	except Exception as e:
		print(e)

def accounts_group_config(accounts:list, browser: Chrome, timeout: int, from_name: str):
	accs_num = len(accounts)
	if accs_num == 0:
		return
	i = 0
	for account in accounts:
		general_settings(browser, timeout, i)
		account_settings(browser, timeout, from_name, i)
		i += 1
		if i < accs_num:
			browser.execute_script('''window.open("about:blank");''')
			browser.switch_to.window(browser.window_handles[i])
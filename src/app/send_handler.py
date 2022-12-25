from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from helpers import browser_handler
from init.init_globals import PATHS, ERRORS
from helpers.logs_handler import Logger

def get_number_of_emails(browser: Chrome, timeout: int):
	xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[1]/div[2]/div[1]/span/div[1]/span'
	acc_info = {'total': 450, 'epp': 50, 'page': 1}
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
		element = browser.find_element(By.XPATH, xpath)
		num = element.text
		_num = num.split('of')
		acc_info['total'] = int(_num[1].strip().replace(',', ''))
		acc_info['epp'] = int(_num[0].split('–')[1].strip().replace(',', ''))
		acc_info['page'] = int(_num[0].split('–')[0].strip().replace(',', ''))
	except Exception as e:
		print(e)
	return acc_info

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

def get_creative(browser: Chrome, timeout: int):
	action = ActionChains(browser)
	xpath ='/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[2]/div/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div/div[2]/div[3]/div/table/tbody/tr/td[2]/div[2]/div/div[1]'
	browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
	element = browser.find_element(By.XPATH, xpath)
	browser.execute_script('window.open("")')
	browser.switch_to.window(browser.window_handles[1])
	browser.get(PATHS.CREATIVE)
	browser_handler.wait_time_in_range(0.7, 1.0)
	action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
	browser_handler.wait_time_in_range(0.2, 0.5)
	action.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
	browser.execute_script('window.close()')
	browser.switch_to.window(browser.window_handles[0])
	element.click()
	browser_handler.wait_time_in_range(0.5, 0.9)
	action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
	browser_handler.wait_time_in_range(0.5, 0.9)
	ActionChains(browser).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()

def send_reply(browser: Chrome, timeout: int):
	xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[4]/div[1]'
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
		element = browser.find_element(By.XPATH, xpath)
		element.click()
		browser_handler.wait_time_in_range(1.1, 1.5)
		get_creative(browser, timeout)
	except Exception as e:
		print(e)

def get_send_date(browser: Chrome, timeout: int, xpath: str):
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
		element = browser.find_element(By.XPATH, xpath)
		email_date = element.get_attribute('aria-label')
		date_compounents = email_date.split(', ')
		day_parse = date_compounents[1].split(' ')
		if len(day_parse[1]) == 1:
			day_parse[1] = '0' + day_parse[1]
		date_compounents[1] = day_parse[0] + ' ' + day_parse[1]
		_date = f'{date_compounents[0]} {date_compounents[1]} {date_compounents[2]}'
		dt = datetime.strptime(_date, '%a %b %d %Y')
		return dt.date()
	except Exception as e:
		print(e)

def is_old_mail(date1: str, date2: datetime.date):
	return datetime.strptime(date1, '%Y-%m-%d').date() <= date2

def back_to_inbox(browser: Chrome, timeout: int):
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div/div[1]/div')
		element = browser.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div/div[1]/div')
		element.click()
	except:
		browser.get('https://mail.google.com/mail/u/0/#inbox')

def get_older_mails(browser: Chrome, timeout: int) -> int:
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[1]/div[2]/div[1]/span/div[3]')
		element = browser.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[1]/div[2]/div[1]/span/div[3]')
		if not element.get_property('disabled'):
			element.click()
			return 1
		return 0
	except:
		return -1

def wait_for_new_page(browser: Chrome, acc_info, timeout: int):
	new_acc_info = get_number_of_emails(browser, timeout)
	while new_acc_info == acc_info:
		browser_handler.wait_time_in_range(1.0, 2.0)
		new_acc_info = get_number_of_emails(browser, timeout)

def send_proccess(browser: Chrome, timeout: int, accepted_from: str, email: str, config):
	acc_info = get_number_of_emails(browser, timeout)
	tbody_xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[8]/div/div[1]/div[2]/div/table/tbody'
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, tbody_xpath)
		i = 0
		while (i:=i+1):
			if i > acc_info['total']:
				break
			j = 0
			if is_old_mail(config['send_date'], get_send_date(browser, timeout, f'{tbody_xpath}/tr[1]/td[8]/span')):
				while (j:=j+1):
					if j > acc_info['epp']:
						break
					element = locate_email(browser, timeout, accepted_from, f'{tbody_xpath}/tr[{j}]/td[4]')
					if element is not None:
						if is_old_mail(config['send_date'], get_send_date(browser, timeout, f'{tbody_xpath}/tr[{j}]/td[8]/span')):
							browser_handler.wait_time_in_range(3.4, 5.5)
							element.click()
							browser_handler.wait_time_in_range(3.4, 5.5)
							send_reply(browser, timeout)
							browser_handler.wait_time_in_range(3.4, 5.5)
							back_to_inbox(browser, timeout)
						else:
							return
			else:
				return
			res = get_older_mails(browser, timeout)
			if res == 0:
				return
			elif res == -1:
				Logger.logger(ERRORS.PROXY_ERROR, email)
				return
			acc_info2 = get_number_of_emails(browser, timeout)
			wait_for_new_page(browser, acc_info2, timeout)
			i = i + acc_info['epp'] - 1
	except Exception as e:
		print(e)
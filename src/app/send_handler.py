from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from helpers import browser_handler, file_hanlder
import pyperclip as pc
from init.init_globals import PATHS

def get_number_of_emails(browser: Chrome, timeout: int):
	xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[1]/div/div[1]/div[2]/div[1]/span/div[1]/span'
	acc_info = {'total': 450, 'epp': 50, 'page': 1}
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
		element = browser.find_element(By.XPATH, xpath)
		num = element.text
		_num = num.split('of')
		acc_info['total'] = int(_num[1].strip())
		acc_info['epp'] = int(_num[0].split('–')[1].strip())
		acc_info['page'] = int(_num[0].split('–')[0].strip())
	except Exception as e:
		print(e)
	return acc_info

def locate_email(browser: Chrome, timeout: int, accepted_from: str, xpath: str) -> WebElement or None:
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
		xpath = f'{xpath}/html/body/div[7]/div[3]/div/div[1]/div[3]/header/div[2]/div[1]/div[4]/div/a'
		element = browser.find_element(By.XPATH, xpath)
		if element.text.lower() == accepted_from.lower():
			return element
		return None
	except:
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
	action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
	browser_handler.wait_time_in_range(0.5, 0.9)
	action.send_keys(Keys.DELETE).perform()
	browser_handler.wait_time_in_range(0.5, 0.9)
	action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
	browser_handler.wait_time_in_range(0.5, 0.9)
	ActionChains(browser).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()



def send_reply(browser: Chrome, timeout: int, accepted_from: str):
	xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td/div[2]/div[2]/div/div[3]/div/div/div/div/div/div[1]/div[2]/div[1]/table/tbody/tr[1]/td[4]/div[1]'
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, xpath)
		element = browser.find_element(By.XPATH, xpath)
		element.click()
		browser_handler.wait_time_in_range(1.1, 1.5)
		get_creative(browser, timeout)

		# script = f"var ele=arguments[0]; ele.innerHTML = '{file_hanlder.read_file_content(PATHS.CREATIVE)}';"
		# print(script)
		# browser.execute_script(script, element)
	except Exception as e:
		print(e)

def send_proccess(browser: Chrome, timeout: int, accepted_from: str, config):
	acc_info = get_number_of_emails(browser, timeout)
	tbody_xpath = '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[8]/div/div[1]/div[2]/div/table/tbody'
	try:
		browser_handler.wait_for_element_by_xpath(browser, timeout, tbody_xpath)
		tbody = browser.find_element(By.XPATH, tbody_xpath)
		i = 0
		while (i:=i+1):
			if i > config['max_send_number']:
				break
			j = 0
			while (j:=j+1):
				if j > acc_info['epp']:
					break
				element = locate_email(browser, timeout, accepted_from, f'{tbody_xpath}/tr[{j}]')
				if element is not None:
					element.click()
					send_reply(browser, timeout, accepted_from)
				browser_handler.wait_time_in_range(200.1, 200.2)
	except Exception as e:
		print(e)
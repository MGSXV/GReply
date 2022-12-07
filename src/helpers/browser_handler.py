from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import random

def simulate_human_typing(text: str, element: WebElement):
	element.clear()
	for char in text:
		wait_time_in_range(1, 3)
		element.send_keys(char)

def wait_for_element_by_id(browser: Chrome, timeout: int, _id: str):
	WebDriverWait(browser, timeout).until(
		EC.presence_of_element_located((By.ID, _id))
		)

def wait_for_element_by_xpath(browser: Chrome, timeout: int, xpath: str):
	WebDriverWait(browser, timeout).until(
		EC.presence_of_element_located((By.XPATH, xpath))
		)

def rand_num_in_range(min, max):
	return random.uniform(min, max)

def wait_time_in_range(min, max):
	sleep(rand_num_in_range(min, max))
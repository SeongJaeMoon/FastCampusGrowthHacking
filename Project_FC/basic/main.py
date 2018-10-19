from selenium import webdriver
import time

DRIVER_DIR = '/Users/temp/Project_FC/chromedriver'

driver = webdriver.Chrome(DRIVER_DIR)
driver.implicitly_wait(10)
driver.get('https://www.google.com')
time.sleep(5)
driver.close()

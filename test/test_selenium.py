from selenium import webdriver

DRIVER_PATH = './chromedriver/'
driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
driver.get('https://google.com')
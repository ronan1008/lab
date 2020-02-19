from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("chromedriver")
driver.implicitly_wait(10)
driver.get("https://www.proex.io/")
register_button = driver.find_element_by_xpath("//div[@class='name']/a[@href='/index.php?m=register']")
register_button.click()

#click register name column
register_username = driver.find_element_by_id('username')
register_username.send_keys('usernametest')
#click register password column
register_password = driver.find_element_by_id('password')
register_password.send_keys('passwordtest')
#click register confirm password column
register_confirm_password = driver.find_element_by_id('confirm_password')
register_confirm_password.send_keys('confirm')






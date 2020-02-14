from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("chromedriver")
driver.implicitly_wait(10)
driver.get("https://www.proex.io/")
register_button = driver.find_element_by_xpath("//div[@class='name']/a[@href='/index.php?m=register']")
register_button.click()



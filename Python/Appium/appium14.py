import time
from appium import webdriver

desired_caps = dict()
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9.0'
desired_caps['deviceName'] = '192.168.244.102:55'
desired_caps['appPackage'] = 'com.android.settings'
desired_caps['appActivity'] = '.Settings'

#默認輸入中文無效，但不會報錯，需要在"前置程式"
desired_caps['unicodeKeyboard'] = True
desired_caps['resetKeyboard'] = True

driver = webdriver.Remote('http://localhost:4723/wd/hub' , desired_caps)
driver.implicitly_wait(10)

B_button = driver.find_element_by_xpath("//*[@text='Battery']")
A_button = driver.find_element_by_xpath("//*[@text='Storage']")

#移動但是有慣性，不適合定位
#driver.scroll(A_button, B_button)

#移動但是沒有慣性
driver.drag_and_drop(A_button, B_button)

time.sleep(5)
driver.quit()
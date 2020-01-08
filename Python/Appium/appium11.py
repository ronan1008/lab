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

#獲取元素位置和大小
search_button = driver.find_element_by_id("com.android.settings:id/search_action_bar_title")
print(search_button.location)
print(search_button.location["x"])
print(search_button.location["y"])
print(search_button.size)
print(search_button.size["width"])
print(search_button.size["height"])
time.sleep(5)
driver.quit()




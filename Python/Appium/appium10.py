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

time.sleep(5)

#2點擊放大鏡
driver.find_element_by_id("com.android.settings:id/search_action_bar").click()
#3輸入 hello
input_label = driver.find_element_by_id("android:id/search_src_text")
input_label.send_keys("hello")
#4暫停2秒
time.sleep(2)
#5清空所有文字內容
input_label.clear()
#6暫停五秒
time.sleep(5)
#7輸入"你好"
driver.quit()
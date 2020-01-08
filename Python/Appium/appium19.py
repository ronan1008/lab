import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.connectiontype import ConnectionType

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

#取得當前畫面的解析度
print(driver.get_window_size())
print(driver.get_window_size()['width'])
print(driver.get_window_size()['height'])

#當下畫面，截圖保存
driver.get_screenshot_as_file("D:\\Downloads\\test.png")

#獲取當前網路狀態
print(driver.network_connection)

#設置當前網路
driver.set_network_connection(4)
time.sleep(1)

#if driver.network_connection ==  ConnectionType.DATA_ONLY:
if driver.network_connection == 4:
    driver.set_network_connection(6)
    print(driver.network_connection)
else:
    print(driver.network_connection)


driver.quit()



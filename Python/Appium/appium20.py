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

#發送按鍵到設備
# https://www.jianshu.com/p/f7ec856ff56f
#三次音量+ 返回 兩次音量-
driver.press_keycode(24)
time.sleep(2)
driver.press_keycode(24)
time.sleep(2)
driver.press_keycode(24)
time.sleep(2)

driver.press_keycode(4)
time.sleep(2)
driver.press_keycode(25)
time.sleep(2)

driver.quit()

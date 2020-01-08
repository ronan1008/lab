import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

desired_caps = dict()
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9.0'
desired_caps['deviceName'] = '192.168.244.102:55'
desired_caps['appPackage'] = 'com.android.settings'
desired_caps['appActivity'] = '.password.ChooseLockPattern'

#默認輸入中文無效，但不會報錯，需要在"前置程式"
desired_caps['unicodeKeyboard'] = True
desired_caps['resetKeyboard'] = True

driver = webdriver.Remote('http://localhost:4723/wd/hub' , desired_caps)
driver.implicitly_wait(10)

TouchAction(driver).press(x=257,y=941).move_to(x=534,y=941)\
            .move_to(x=818,y=941).move_to(x=818,y=1226)\
            .move_to(x=541,y=1226).move_to(x=257,y=1226)\
            .move_to(x=541,y=1501).release().perform()
time.sleep(5)
driver.quit()



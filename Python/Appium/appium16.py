import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

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

lan_button = driver.find_element_by_xpath("//*[@text='Network & internet']")
#高級手勢 : press 和 release
#1.創建 touchaction 對象
#2.調用動作
#3.使用perform執行動作

TouchAction(driver).press(x=750, y=750).perform()
time.sleep(2)
TouchAction(driver).press(x=750, y=750).release().perform()
time.sleep(5)
driver.quit()
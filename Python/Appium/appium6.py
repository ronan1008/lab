from appium import webdriver
import time
desired_caps = dict()

desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9.0'
desired_caps['deviceName'] = '192.168.244.102:55'
desired_caps['appPackage'] = 'com.android.settings'
desired_caps['appActivity'] = '.Settings'
driver = webdriver.Remote('http://localhost:4723/wd/hub' , desired_caps)



# 通過id定位放大鏡 然後點擊
driver.find_element_by_id("com.android.settings:id/search_action_bar").click()

#通過class定位輸入 hello
driver.find_element_by_class_name("android.widget.EditText").send_keys("hello")

#通過xpath定位 返回按鈕，點擊
driver.find_element_by_xpath("//*[@content-desc='Navigate up']").click()

time.sleep(5)
driver.quit()

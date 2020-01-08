from appium import webdriver
import time
desired_caps = dict()

desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9.0'
#android 設備名稱 可以隨意,ios不能隨便寫 例如:iphone6
desired_caps['deviceName'] = '192.168.244.102:55'
desired_caps['appPackage'] = 'com.android.settings'
desired_caps['appActivity'] = '.Settings'

#0.0.0.0 = 127.0.0.1 = localhost
driver = webdriver.Remote('http://localhost:4723/wd/hub' , desired_caps)


time.sleep(5)

#跳轉到另外一個APP

#輸出當前的 package name 
print(driver.current_package)
#輸出當前的 activity name
print(driver.current_activity)

#跳轉到另外一個APP
driver.start_activity('com.android.messaging', '.ui.conversationlist.ConversationListActivity')

driver.quit()

from appium import webdriver
import time
desired_caps = dict()

desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9.0'
#android 設備名稱 可以隨意,ios不能隨便寫 例如:iphone6
desired_caps['deviceName'] = '192.168.244.102:55'
#desired_caps['appPackage'] = 'com.android.settings'
#desired_caps['appActivity'] = '.Settings'

desired_caps['appPackage'] = 'com.android.messaging'
desired_caps['appActivity'] = '.ui.conversationlist.ConversationListActivity'


#0.0.0.0 = 127.0.0.1 = localhost
driver = webdriver.Remote('http://localhost:4723/wd/hub' , desired_caps)

print('-----準備進入後台-----')

#進入後台五秒鐘，再回到前台
driver.background_app(5)

print('-----已經回到前台-----')
time.sleep(5)
driver.quit()
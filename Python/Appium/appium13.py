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

#從(x,y)移動到(x,y)，每一次滑動可能有誤差
driver.swipe(100,2000,100,1000)

#從(x,y)移動到(x,y)，持續五秒，類似變成緩慢移動，誤差變小
driver.swipe(100,2000,100,1000,5000)




time.sleep(25)
driver.quit()


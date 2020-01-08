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

time.sleep(3)

#關閉當前對象APP，但是Driver還在
driver.close_app()

#關閉Driver，同時關閉所有關聯的APP
#driver.quit()
print(driver.current_package)
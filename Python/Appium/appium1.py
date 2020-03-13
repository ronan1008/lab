from appium import webdriver
import time
desired_caps = dict()

desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '10.0'
desired_caps['deviceName'] = 'PNXGAM8932802833'
#desired_caps['appPackage'] = 'com.android.settings'
#desired_caps['appActivity'] = '.Settings'

desired_caps['appPackage'] = 'com.asiainnovations.ace.taiwan'
desired_caps['appActivity'] = 'com.asiainnovations.ace.splash.SplashActivity'



#0.0.0.0 = 127.0.0.1 = localhost
driver = webdriver.Remote('http://localhost:4723/wd/hub' , desired_caps)


time.sleep(5)

driver.quit()


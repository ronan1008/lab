import time
from appium import webdriver

desired_caps = dict()

desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9.0'
desired_caps['deviceName'] = '192.168.244.102:55'
desired_caps['appPackage'] = 'com.android.settings'
desired_caps['appActivity'] = '.Settings'
driver = webdriver.Remote('http://localhost:4723/wd/hub' , desired_caps)

#隱式等待，設置時間之後，後續所有定位的元素方法都會在這個時間內等待元素的出現
#如果出現了，直接進行後續的操作
#如果沒有出現，報錯，NoSuchElementException。

driver.implicitly_wait(20)

print('---準備返回並點擊')

driver.find_element_by_xpath("//*[@content-desc='Navigate up']").click()

print('---點完')

time.sleep(5)
driver.quit()



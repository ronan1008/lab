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

eles = driver.find_elements_by_id("android:id/title")

for i in eles:
    print(i.get_attribute("text"))
    print(i.get_attribute("enabled"))
    print(i.get_attribute("clickable"))
    print(i.get_attribute("checked"))
    #底下有特殊的寫法
    #EX1: value='name'返回 content-desc/text屬性值
    #EX2: value='className'返回class屬性值，只有API=>18才有
    #EX3: value='resourceId'返回resource-id屬性值，只有API=>18才有
    print(i.get_attribute("resourceId"))
    print(i.get_attribute("className"))
    print(i.get_attribute("name"))
    print('-'*10)
print("="*20)
eles = driver.find_elements_by_class_name("android.widget.TextView")

for i in eles:
    print(i.get_attribute('text'))
    print(i.get_attribute('name'))


time.sleep(5)
driver.quit()


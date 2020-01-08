from appium import webdriver
import time
desired_caps = dict()

desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9.0'
desired_caps['deviceName'] = '192.168.244.102:55'
desired_caps['appPackage'] = 'com.android.settings'
desired_caps['appActivity'] = '.Settings'
driver = webdriver.Remote('http://localhost:4723/wd/hub' , desired_caps)

time.sleep(5)

#找出所有符合id的元素
titles = driver.find_elements_by_id("android:id/title")
print(titles)
print(len(titles))


#找出所有符合class的元素，如果傳錯了，會報錯誤，找不到
textviews = driver.find_elements_by_class_name("android.widget.TextView")
for textview in textviews:
    print(textview.text)
print(len(textviews))

#找出所有符合xpath的元素，如果傳錯了，回傳一個空列表
eles = driver.find_elements_by_xpath("//*[contains(@text,'S')]")

for ele in eles:
    print(ele.text)
print(len(eles))
driver.quit()

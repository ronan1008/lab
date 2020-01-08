import time
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait



desired_caps = dict()
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9.0'
desired_caps['deviceName'] = '192.168.244.102:55'
desired_caps['appPackage'] = 'com.android.settings'
desired_caps['appActivity'] = '.Settings'
driver = webdriver.Remote('http://localhost:4723/wd/hub' , desired_caps)


print('---準備返回並點擊')
#顯式等待
#關鍵類 : WebDriverWait
#關鍵方法 : WebDriverWait對象中的 until 的方法
#設置了顯式等待之後，可以等待一個超時時間，在這個時間內查找，默認以每0.5秒找一次
#0.5秒頻率可以改
#一但找到這個元素，直接進行後續的操作
#如果沒有找到，報錯，TimeOutException
back_button = WebDriverWait(driver, 5, 1).until(lambda x: x.find_element_by_xpath("//*[@content-desc='Navigate up']"))
back_button.click()
print('---點完')

time.sleep(5)
driver.quit()
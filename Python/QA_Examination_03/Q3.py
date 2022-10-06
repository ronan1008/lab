# Enter your code here.
import csv
import requests
import time
import sys
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from configparser import ConfigParser

def open_browser(visual):
    mobile_emulation = {
    # "deviceMetrics": { "width": 360, "height": 800, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
    chrome_options = Options()
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = {'performance': 'ALL'}
    if not visual :
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("disable-dev-shm-usage")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument('--disk-cache-dir=/home/shocklee/temp')
    chrome_options.add_experimental_option("detach", False)

    driver = webdriver.Chrome(desired_capabilities=d, options=chrome_options)
    driver.implicitly_wait(10)
    return driver

def api(prefix, head, apiName, way, body):
    resquestDic = {
        'post':requests.post,
        'put':requests.put,
        'patch':requests.patch,
        'get':requests.get,
        'delete':requests.delete}
    url = prefix + apiName
    res = resquestDic[way](url, headers=head)
    return res


#Q1
def Q1():
    with open('login_log.csv', newline='') as f:
        reader = csv.reader(f)
        data = [tuple(row) for row in reader]

    error_list= []

    for i, data_row in enumerate(data):

        if i == 0:
            continue
        else:
            uid, phone, user_type, login_count = data_row[0], data_row[1], data_row[2], int(data_row[3])

        if phone[0:4] == '+886':
            if user_type == 'unregistered' and login_count > 0:
                error_list.append(data_row)
            if login_count < 0 or login_count > 100000:
                error_list.append(data_row)

    pprint(error_list)

#Q2

def Q2():
    SQL = '''
SELECT
	Movies.Title,
	Boxoffice.Domestic_sales,
	Boxoffice.International_sales
FROM
	Movies
	JOIN Boxoffice ON Movies.id = Boxoffice.Movie_id
ORDER BY
	Movies.Title DESC
'''
    print(SQL)



#Q3

def Q3():
    prefix = 'https://cdn.jsdelivr.net'
    apiName = '/gh/fawazahmed0/currency-api@1/2021-08-01/currencies/twd.json'
    header = {'Content-Type': 'application/json', 'Connection': 'Keep-alive'}
    # apiName = requests.compat.quote_plus(apiName)
    res = api(prefix, header, apiName, 'get', body=None)

    result_dic = {}
    date_range = ['2021-08-01', '2021-08-02', '2021-08-03', '2021-08-04', '2021-08-05', '2021-08-06', '2021-08-07']
    for date in date_range:
        apiName = '/gh/fawazahmed0/currency-api@1/{}/currencies/twd.json'.format(date)
        res = api(prefix, header, apiName, 'get', body=None)
        restext = res.json()
        date = restext['date']
        TWD_to_JP = restext['twd']['jpy']
        result_dic[date] = TWD_to_JP


    tw_jp = {'date': [date for date in result_dic.keys()],
                'ex_rate': [ex_rate for ex_rate in result_dic.values()]}

    tw_jp_df = pd.DataFrame(
        tw_jp, columns=['ex_rate'], index=tw_jp['date'])
    ax = tw_jp_df.plot(title='exchange_rate', kind='line',
                                fontsize=10, figsize=(15, 5))
    for i in ax.patches:
        ax.text(i.get_width()+100, i.get_y()+0.15,
                i.get_width(), fontsize=10, color='red')
    plt.ylabel('exchange_rate')
    plt.xlabel("date")
    plt.show()



# #Q4


def Q4():
    #read config file
    config = ConfigParser()
    config.read('104_acc_pass.ini')


    identity = config.get('Enviroment', 'ID')
    password = config.get('Enviroment', 'PASS')

    if not (identity or password):
        print("please input 104_acc_pass.ini identity and pass")
        sys.exit(1)
    driver = open_browser(True)
    driver.get('https://www.104.com.tw/jobs/main/')
    login_btn = driver.find_element_by_xpath('//a[text()="登入"]')
    login_btn.click()

    page_elmt = driver.find_element_by_xpath('//main')
    page = page_elmt.get_attribute('innerHTML')

    account_col = driver.find_element_by_xpath('//input[@id="username"]')
    account_col.send_keys(identity)

    password_col = driver.find_element_by_xpath('//input[@id="password"]')
    password_col.send_keys(password)

    submit_btn = driver.find_element_by_xpath('//button[@id="submitBtn"]')
    submit_btn.click()

    myname = driver.find_element_by_xpath('//p[@id="myName"]')
    myname.click()

    member_center = driver.find_element_by_xpath('//a[text()="My104會員中心"]')
    member_center.click()
    new_window  = driver.window_handles[1]
    driver.switch_to.window(new_window)
    member_name_ele = driver.find_element_by_xpath('//div[@class="h2 mb-3"]')
    member_name = member_name_ele.text
    pprint(member_name)

    if member_name:
        member_center = driver.find_element_by_xpath('//a[text()="登出"]')
        member_center.click()
        print("找到姓名: {}".format(member_name))
    else:
        print("沒找到姓名")
    time.sleep(3)
    driver.quit()



if __name__ == '__main__':
    print('this is for job exam')
    print('第1題答案')
    Q1()
    print('第2題答案')
    Q2()
    print('第3題答案，使用 pandas 與 matplotlib')
    Q3()
    print('第4題答案')
    Q4()



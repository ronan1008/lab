#!/usr/bin/env python
# coding: utf-8

# In[91]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pyquery import PyQuery as pq
import pprint
import sys
import time
import requests
from IPython.core.display import display, HTML


infos = []

def quickInputDestination() :
    desDic = {'1':'京都 日本','2':'東京 日本','3':'台北 台灣' ,'4':'台中 台灣'}
    desStr = ''
    for num,des in desDic.items():
        desStr += "{}.{} ".format(num,des) 
    dest= input("請輸入數字，例如: {} 或是直接輸入地名".format(desStr))
    if dest in desDic.keys():
        dest = desDic[dest]
    else:
        dest = dest
    
    infos.append("目的地："+dest)
    return dest
    
destination = quickInputDestination()

checkInOutDate = input("請輸入check-in&out日期, EX：2020-04-01 2020-04-05 : ")
infos.append("check-in & out日期："+checkInOutDate)
checkInDate,checkOutDate = checkInOutDate.split()

rooms = input("請輸入需要的房間數量")
infos.append("房間數量:"+rooms)
roomsOfPeopleList = []
for room in range(int(rooms)):
    howPeople= input("請輸入第{}間房:幾大幾小 , EX :2 1-->".format(room+1)).split()
    infos.append("第{}間房:{}大{}小".format(room+1,howPeople[0],howPeople[1]))
    roomsOfPeopleList.append(howPeople)
    
for info in infos:
    print("\x1b[31m{}\x1b[0m".format(info))
correct = input("請確認以上資料正確嗎？不正確輸入n，正確輸入任意字元")
if correct == 'n':
    sys.exit("請重新輸入") 

driver = webdriver.Chrome("chromedriver")
driver.get("https://tw.hotels.com")
###close the popup window
if driver.find_elements_by_css_selector('#managed-overlay > button'):
    driver.find_element_by_css_selector('#managed-overlay > button').click()
###click destination input column
driver.find_element_by_css_selector('#qf-0q-destination').send_keys(destination)

webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
time.sleep(1)
###wait element is clickable
# driver.find_element_by_css_selector('div.hero-container po-r').click()
# wait = WebDriverWait(driver,10)
# element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cta.cta-link")))
# element.click()

checkInCol = driver.find_element_by_css_selector('#qf-0q-localised-check-in')
checkInCol.clear()
checkInCol.click()
checkInCol.send_keys(checkInDate)
checkOutCol = driver.find_element_by_css_selector('#qf-0q-localised-check-out')
checkOutCol.clear()
checkOutCol.click()
checkOutCol.send_keys(checkOutDate)
driver.find_element_by_css_selector('button.widget-overlay-close').click()

s1 = Select(driver.find_element_by_css_selector('#qf-0q-compact-occupancy')) 
s1.select_by_index(2)

s1 = Select(driver.find_element_by_css_selector('select.query-rooms')) 
s1.select_by_value(rooms) 
for roomOfPeople in range(len(roomsOfPeopleList)):
    adults,children = roomsOfPeopleList[roomOfPeople]
    s1 = Select(driver.find_element_by_css_selector('#qf-0q-room-{}-adults'.format(roomOfPeople))) 
    s1.select_by_value(adults)
    if children != '':
        s1 = Select(driver.find_element_by_css_selector('#qf-0q-room-{}-children'.format(roomOfPeople))) 
        s1.select_by_value(children) 

#click search button
driver.find_element_by_css_selector('button.cta.cta-strong').click();
driver.current_url
time.sleep(6)
####################################################################


# In[92]:


html = driver.find_element_by_css_selector("*").get_attribute("outerHTML")
doc = pq(html)


def leftCheckbox(title):

    panelTitle = doc("h3:contains("+title+")")

    if title=="星級評等":
        panelTitleParent =  panelTitle.parent(".filter-legend+div li label span:nth-child(2):contains('星級')")
    elif title=="設施":
        panelTitleParent =  panelTitle.parent(".filter-legend+div#filter-facilities-contents li")
    else: 
        panelTitleParent  =  panelTitle.parent(".filter-legend+div li")

    choList = []
    for i in panelTitleParent.items():
        choList.append(i.text())
    choStr=','.join(choList)

    print('請從 {} 選擇：'.format(title))
    print(choStr)
 
    conInput = input()
    if conInput == '':
        return 0
    userChecks = conInput.split(',')
    
    ###check if the columns is collapsed
    panelTitle = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, "//h3[text()='{}']".format(title)))    
    )
    checkTitle = driver.find_element_by_xpath("//h3[text()='{}']/../..".format(title))
    checkTitle = checkTitle.get_attribute("class")
#     panelTitle = driver.find_element_by_xpath("//h3[text()='{}']".format(title))
#     checkTitle = panelTitle.get_attribute("aria-expanded")
    if checkTitle == 'checkbox-filters filter-collapsed':
        print("click....panel")
        panelTitle.click()
    ####################################
    
    for i in userChecks: 

        if title == "星級評等" :
            check=driver.find_element_by_xpath("//span[text()='{}']/../preceding-sibling::input".format(i))

        else: 
            check=driver.find_element_by_xpath("//label[text()='{}']/preceding-sibling::input".format(i))
        check.click()

    time.sleep(5)

def leftControlPanel(title):

    if title == "每晚價格":
        minVal,maxVal = input("請輸入 每晚價格 的價格區間，EX:1250,6500 ").split(',')
        minVal=int(minVal)
        maxVal=int(maxVal)
        leftSteps = minVal//250
        rightSteps = (25000-maxVal)//250 
        startPoint = driver.find_element_by_xpath("//h3[text()='{}']/../following-sibling::div/div/div/div[contains(@class,'widget-slider-handle-min')]".format(title))
        endPoint = driver.find_element_by_xpath("//h3[text()='{}']/../following-sibling::div/div/div/div[contains(@class,'widget-slider-handle-max')]".format(title))
        
    elif title == "旅客評分":
        minVal,maxVal = input("請輸入 旅客評分 的評分區間，EX:7,10 ").split(',')
        minVal=int(minVal)
        maxVal=int(maxVal)
        leftSteps = minVal
        rightSteps = 10-maxVal
        startPoint = driver.find_element_by_xpath("//h3[text()='{}']/following-sibling::div/div/div/div[contains(@class,'widget-slider-handle-min')]".format(title))
        endPoint = driver.find_element_by_xpath("//h3[text()='{}']/following-sibling::div/div/div/div[contains(@class,'widget-slider-handle-max')]".format(title))
        
    for i in range(leftSteps):
        startPoint.send_keys(Keys.RIGHT)
    for k in range(rightSteps):
        endPoint.send_keys(Keys.LEFT)
    time.sleep(5)
leftCheckbox("星級評等")
leftCheckbox("區域")
#leftPanelCheck("設施")

leftControlPanel("每晚價格")
leftControlPanel("旅客評分")
print ('Page Filter Done...')


# In[93]:


from pprint import pprint
wrapper=driver.find_element_by_css_selector("body > div#main-content")
last_height = -1
while True:
    heightVal = wrapper.size["height"]
    print ('Loading Page...')
    if last_height == heightVal:
        print ('Loading Page Done...')
        break
    last_height = heightVal
    driver.execute_script("window.scrollTo({},{})".format(0,heightVal))
    time.sleep(8)
    
html = driver.find_element_by_css_selector("*").get_attribute("outerHTML")
response = requests.get(driver.current_url)
doc = pq(html)
doc.make_links_absolute(base_url=response.url)
mainHtml=doc("li.hotel")
tableHeader = "<table id='myTable' class='tablesorter-blue' >"
tableTitle = "<thead><tr><td style='text-align:left;'>飯店</td><td>特價</td><td>原價</td><td width='80'>位置</td><td width='180' style='text-align:left';>距離</td><td width='120'>評價</td><td width='80'>評語數量</td><td width='130'>地址</td></tr></thead><tbody>"
tableFooter = "</tbody></table>"
tableBodyList=[]
hotelCount = 0 
hotelInfoList=[]
for i in mainHtml.items():
    
    hotelName = i("h3.p-name").html()
 
    reviews = i("div.reviews-box strong.guest-reviews-badge").html()
    reviews=float(reviews[-3:])
    reviewsCount = i("div.reviews-box a span.small-view").html()
    reviewsCount = reviewsCount.replace("則評語",'')
    location = i("div.additional-details div.location-info a").html()
    distance = i("div.additional-details div.location-info ul.property-landmarks").html() 
    address = i("span.address").text()
    specialPrice = i("div.price a del").text() or ''  
    actualPrice = i("div.price a ins").html() or i("div.price a strong").html()

    if actualPrice is None: 
        actualPrice = '<strong>銷售一空</strong>'
    else:
        price = actualPrice.replace("NT$", '')
        price = price.replace(",", '')
        hotelInfoList.append(((hotelName),(price),(specialPrice),(location),(distance),(reviews),(reviewsCount),(address)))       
    #tableBodyList.append("<tr> <td class='left'>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> </tr>".format(hotelName,actualPrice,specialPrice,location,distance,reviews,reviewsCount,address))
    
    hotelCount += 1


#sort by price
hotelInfoList.sort(key=lambda x:x[1])

for hotelInfo in hotelInfoList:
    tableBodyList.append("<tr> <td  style='text-align:left;'>{}</td> <td>NT${:,}</td> <td><del>{}</del></td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> </tr>".format(hotelInfo[0],int(hotelInfo[1]),hotelInfo[2],hotelInfo[3],hotelInfo[4],hotelInfo[5],hotelInfo[6],hotelInfo[7]))
    
script ="<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js\"></script><script src=\"https://mottie.github.io/tablesorter/dist/js/jquery.tablesorter.min.js\"></script><script>$(function() {  $(\"#myTable\").tablesorter();\
});\
</script>"
css="<link rel=stylesheet type=\"text/css\" href=\"table.css\">"

display(HTML("{}".format(script)))
display(HTML("{}".format(css)))   
  
display(HTML("<strong>一共有<font size='5' color='red'>{}</font>筆飯店</strong>".format(hotelCount)))
    
tableBody = ''.join(tableBodyList)
                
display(HTML(tableHeader+tableTitle+tableBody+tableFooter))
with open("hotels.html" , 'w' ) as fileObj:
    fileObj.write(script+'\n')
    fileObj.write(css+'\n')
    fileObj.write(tableHeader+tableTitle+tableBody+tableFooter)




# In[94]:


import time
import requests
import random
from pyquery import PyQuery as pq
from IPython.core.display import display, HTML
###########################
from linebot import LineBotApi
from linebot.models import TextSendMessage
line_bot_api = LineBotApi('DU6zE3IPG4bRtdk8pfNlfIEmEY4mC7dD8HLj9B6Ot16IPJBPWWD7tSlq0NpPc1W+EkJ5zF00AE+RRgBQPzUeebm14TBEBhGW3VS2sMzKQYr9rwp7J5xRcijQBmK3BPbQ+b3DgnBAryhIDRdUCAm+rQdB04t89/1O/w1cDnyilFU=')

###########################
with open("hotels.html") as f:
       content = f.read()
trackList = input("關注飯店的keyword,EX: 京都三條飯店,京都東山丸福飯店,河原町二條多夫飯店,優遊 Inn").split(',')

formatList =[]
for i in trackList:
    formatList.append('a:contains("{}")'.format(i))
    
FilterStr = ','.join(formatList)
doc = pq(content)
aTag=doc(FilterStr)
hotelDictTrack={}
#print(aTag)
messageLine = ''
for i in aTag.items():
    hotelDictTrack[i.text()]=i.attr('href')

def trackHotelDic(hotelDic,times,interval):
    original={}
    for i in range(times):
        i =i+1
        print('第{}次監控價格'.format(i))
        for hotel,url in hotelDic.items():
            response = requests.get(url)
            doc = pq(response.text)
            price=doc("span.current-price").text()
            price = int(price.replace("NT$",'').replace(',',""))
            ######for test only
            if i==3:
                price = price - random.randint(100,400)
                
            if i==2:
                price = price + random.randint(100,400)
            ######
            #.replace(',',"")
            if i==1:
                original[hotel] = price
                print('{} \t開始監控 現價是 : {}'.format(hotel,original[hotel]))
            elif price < original[hotel]:
                messageLine = '{} \t\x1b[31m出現特價\x1b[0m 現價 : {}, 原價 : {} 網址 : {}'.format(hotel,price,original[hotel],url)
                line_bot_api.push_message('U64843a4ebd4abcce420232ea4da7966e', 
    TextSendMessage(text=messageLine))
                print(messageLine)
            elif price > original[hotel]:
                print('{} \t漲價了  : {}, 原價{}'.format(hotel,price,original[hotel]))
            else:
                print('{} \t價格沒有變化 與原價相等'.format(hotel))
        print('')
        time.sleep(interval)
        
trackHotelDic(hotelDictTrack,5,10)
#aTag.attr('href')

#doc("a:contains('梅田')").parents()


# In[ ]:





# In[ ]:





# In[95]:


import time
import requests
from pyquery import PyQuery as pq
from IPython.core.display import display, HTML
url ='https://www.callingtaiwan.com.tw/blog/hotels-com-agoda-hotelclub-expedia-coupon-2014/'


# In[96]:


response = requests.get(url)
doc = pq(response.text)
couponList = doc("h2:contains('Hotels.com 優惠碼')+ul>li:contains('台灣')") 
tableHeader = "<table>"
tableTitle = "<thead><tr><td style='text-align:left;'>coupon優惠</td><td>coupon</td></tr></thead><tbody>"
tableFooter = "</tbody></table>"
tableBodyList=[]
for i in couponList.items():
    coupon = i("a.rdc_box_button").text()
    i("a:contains('點此前往Hotels.com台灣')").remove()
    i("a.rdc_box_button").remove()
    description = i
    tableBodyList.append("<tr> <td style='text-align:left;'>{}</td> <td>{}</td> </tr>".format(description,coupon))

css="<link rel=stylesheet type=\"text/css\" href=\"table.css\">"
display(HTML("{}".format(css)))  
tableBody = ''.join(tableBodyList)                
display(HTML(tableHeader+tableTitle+tableBody+tableFooter))


tableTitle = "<thead><tr><td  style='text-align:left;'>信用卡優惠</td></tr></thead><tbody>"
tableFooter = "</tbody></table>"
tableBodyList=[]
creditList = doc("h2:contains('信用卡')+p+ul>li:contains('台灣')") 

creditAllowList = ["Master","Visa","中國","玉山","富邦"]
creditFilter = []
for credit in creditAllowList:
    creditFilter.append("li:contains({})".format(credit))
creditFilter = ','.join(creditFilter)
#creditList = creditList('li:contains("Master"), li:contains("中國"), li:contains("玉山"), li:contains("富邦"), li:contains("Visa")')
creditList = creditList(creditFilter)
for i in creditList.items():
    tableBodyList.append("<tr> <td style='text-align:left;'>{}</td> </tr>".format(i))
tableBody = ''.join(tableBodyList) 
display(HTML(tableHeader+tableTitle+tableBody+tableFooter))   


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[1]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





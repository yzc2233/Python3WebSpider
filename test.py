import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


url = 'http://10.157.24.132:10016/swagger-ui.html'

option = webdriver.firefox.options.Options()
option.add_argument('-headless')#无头模式
browser = webdriver.Firefox(firefox_options=option)
browser.get(url)
wait = WebDriverWait(browser,10)
wait.until(EC.presence_of_element_located((By.ID,'resources')))
data = browser.page_source
# print(data)
datahtml = BeautifulSoup(data,'html.parser')
# ApiControlList = datahtml.find_all(class_='endpoints',attrs={'style':'display: block;'})
ApiControlList = datahtml.select("ul>li>ul>li>ul>li .heading")
print(ApiControlList)

# for ApiControl in ApiControlList:
#     ApiList = ApiControl.find_all(name='div',class_='heading')
#     print(ApiList)





browser.close()














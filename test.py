import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


url = 'http://10.157.24.142:10016/swagger-ui.html'
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Host':'10.157.24.142:10016',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.17 Safari/537.36'
}

option = webdriver.ChromeOptions()
option.add_argument('headless')
browser = webdriver.Chrome(chrome_options=option)
browser.get(url)
wait = WebDriverWait(browser,3)
wait.until(EC.presence_of_element_located((By.ID,'resource_behavior45post45controller')))
data = browser.page_source
# print(data)

reqtype = browser.find_element_by_xpath('/html/body/div[3]/div[2]/ul/li[1]/ul/li[1]/ul/li/div[1]/h3/span[1]/a')
print(str(reqtype.text))







browser.close()














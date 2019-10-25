import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


url = 'http://10.157.24.142:10016/swagger-ui.html'
url2 = 'http://10.157.24.142:10016/swagger-resources/configuration/security'
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
headers2 = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Host':'10.157.24.142:10016',
    'Referer':'http://10.157.24.142:10016/swagger-ui.html',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.17 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
}

browser = webdriver.Chrome()

# req = requests.get(url,headers=headers)
# req2 = requests.get(url2,headers=headers2)
# req3 = requests.get(url,headers=headers)
browser.get(url)
wait = WebDriverWait(browser,10)
wait.until(EC.presence_of_element_located((By.ID,'resource_behavior45post45controller')))
browser.close()
print(browser.page_source)

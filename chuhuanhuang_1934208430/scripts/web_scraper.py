from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

import os

#set chromeDriver
chrome_options = webdriver.ChromeOptions()
#ubuntu setting
chrome_options.add_argument("--headless=new")  

cdriver = Service(executable_path = './chromedriver')
driver = webdriver.Chrome(service = cdriver, options = chrome_options)

#crawl the link
url = "https://www.cnbc.com/world/?region=world"
driver.get(url)

#wait 10 secs
wait = WebDriverWait(driver, 30)
wait.until(EC.presence_of_element_located((By.ID, "market-data-scroll-container")))
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".LatestNews-container")))

#html save
content = driver.page_source
with open("../data/raw_data/web_data.html", "w", encoding = "utf-8") as f:
    f.write(content)

#close the tab
driver.quit()

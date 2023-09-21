# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

import pandas
import csv
import time
import requests
from bs4 import BeautifulSoup

url = "https://www.youtube.com/@PCBuilderBangladesh/videos"
driver.get(url)

driver.minimize_window()

for i in range(20):
    time.sleep(3)
    driver.find_element(By.TAG_NAME, ("body")).send_keys(Keys.END)

data = [["Title", "Views", "Time"]]

html = driver.page_source

soup = BeautifulSoup(html, "lxml")
videos = soup.find_all("div", {"id": "dismissible"})

for video in videos:
    title = video.find("a", {"id": "video-title-link"}).text
    views_and_before = video.find_all("span", {"class", "inline-metadata-item style-scope ytd-video-meta-block"})
    views = views_and_before[0].text
    before = views_and_before[1].text
    data.append([title, views, before])

data_frame = pandas.DataFrame(data)
data_frame.to_csv("sample data.csv", index=False, index_label=False)

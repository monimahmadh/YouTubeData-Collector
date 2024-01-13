# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up Chrome WebDriver with options
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Define YouTube channel URL
url = "https://www.youtube.com/@PCBuilderBangladesh/videos"
driver.get(url)


# Scroll down 23 times to load more videos
for i in range(23):
    time.sleep(3)
    driver.find_element(By.TAG_NAME, ("body")).send_keys(Keys.END)

# Extract HTML content from the page
html = driver.page_source

# Parse HTML content using BeautifulSoup
soup = BeautifulSoup(html, "lxml")
videos = soup.find_all("div", {"id": "dismissible"})

# Extract video information and store in a list
data = [["Title", "Views", "Time"]]
for video in videos:
    title = video.find("a", {"id": "video-title-link"}).text
    views_and_before = video.find_all("span", {"class", "inline-metadata-item style-scope ytd-video-meta-block"})
    views = views_and_before[0].text
    before = views_and_before[1].text
    data.append([title, views, before])

# Create a DataFrame from the extracted data
data_frame = pd.DataFrame(data)

# Save the DataFrame to a CSV file
data_frame.to_csv("sample_data.csv", index=False, index_label=False)

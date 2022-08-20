from selenium import webdriver
from selenium.webdriver import ChromeOptions
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import webbrowser as wb
import os

url = "https://wallpapers.com/search/"

#s = Service(ChromeDriverManager().install())
opt = ChromeOptions()
opt.add_argument('--headless')
opt.add_argument('--no-sandbox')
opt.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=opt)

def get_images(query: str):
    search = url + query
    try:
        driver.get(search)
        images = driver.find_elements(By.CLASS_NAME, 'lozad')
        for i in images:
            src = i.get_attribute('src')
            new_src = src.replace('thumb', 'file')
            yield {"type": 'photo',"media": new_src}
        driver.close()
    except:
        driver
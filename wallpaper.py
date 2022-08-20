from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import webbrowser as wb

url = "https://wallpapers.com/search/"

s = Service(ChromeDriverManager().install())
opt = Options()
opt.add_argument('--headless')
opt.add_argument('--no-sandbox')
opt.add_argument('--incognito')
driver = webdriver.Chrome(options=opt, service=s)

def get_images(query: str):
    search = url + query
    driver.get(search)
    images = driver.find_elements(By.CLASS_NAME, 'lozad')
    for i in images:
        src = i.get_attribute('src')
        new_src = src.replace('thumb', 'file')
        yield {"type": 'photo',"media": new_src}
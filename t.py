import requests
from bs4 import BeautifulSoup as bs

def get_images(query):
    res = requests.get(f'https://wallpapers.com/search/{query}', stream=True)
    if res.status_code == 200:
        soup = bs(res.content, 'html.parser')
        imgs = soup.select('.lozad')
        for i in imgs:
            src = ('https://wallpapers.com' + i['src'])
            new_src = src.replace('thumb', 'file')
            yield {
                "type": "photo",
                "media": new_src
            }
    else:
        return 'Error'
        
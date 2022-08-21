import requests
from bs4 import BeautifulSoup as bs

def get_images(query):
    res = requests.get(f'https://wallpapers.com/search/{query}')
    if res.status_code == 200:
        soup = bs(res.content, 'html.parser')
        imgs = soup.select('.lozad')
        if len(imgs) > 0:
            for i in imgs:
                try:
                    src = 'https://wallpapers.com' + i['src']
                except Exception as e:
                    src = 'https://wallpapers.com' + i['data-src']
                new_src = src.replace('thumb', 'file')
                code = new_src[len(new_src)-21:len(new_src)-4]
                new_src = new_src[:len(new_src)-21]+(code*2)+new_src[len(new_src)-4:]
                yield {
                    "type": "photo",
                    "media": new_src
                }
        else:
            return imgs
    else:
        return False
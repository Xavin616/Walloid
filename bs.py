import requests
from bs4 import BeautifulSoup as bs

url = 'https://wallpapers.com/search/{query}/'
url2 = url+'page/{page}'

def get_images(query):
    res = requests.get(url.format(query=query))
    if res.status_code == 200:
        soup = bs(res.content, 'html.parser')
        number = soup.select(".d-flex")
        no_of_walls = (((number[5]).select_one('p')).text).replace('Wallpapers', '')
        nom = int(no_of_walls.strip())
        no_pages = nom//10
        imglist = []
        for i in range(0,3):
            x = [img for img in get_page_images(query, str(i))]
            if len(x) < 0:
                continue
            imglist.append(x)
        return imglist

def get_page_images(query, page_no):
    if page_no == 1:
        res = requests.get(url.format(query=query))
    else:
        res = requests.get(url2.format(query=query, page=page_no))
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

if __name__ == "__main__":
    for i in get_images('harley'):
        print(i, '\n')
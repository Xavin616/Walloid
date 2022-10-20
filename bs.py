import requests
from bs4 import BeautifulSoup as bs

url = 'https://wallpapers.com/search/{query}/'
url2 = url+'page/{page}'

def chunk(array, num):
    for i in range(0, len(array), num):
        yield array[i:i+num]

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

def get_images(query):
    imglist = []
    for i in range(0,1):
        x = [img for img in get_page_images(query, str(i))]
        for i in chunk(x, 10):
            # print(f"List: {y.index(i)} Found {len(i)} images.")
            imglist.append(i)
    return imglist[:3]

if __name__ == "__main__":
    x = [i for i in get_images('neon')]
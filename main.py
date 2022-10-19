from flask import Flask, Response, request
from requests import get, post
import json
from bs import get_images

app = Flask(__name__)

token = "5769955382:AAGfR5d6500c_R1E9q1iSRQfvx4GjFitaUU"
telegram_api = f"https://api.telegram.org/bot{token}"

welcome = """You summoned me, @{user} I am Walloid, keeper of HD wallpapers.
Use 'search <Your query>' to search for wallpapers, do not stray from this rule for there will be dire consequences.
To add me to a group, use:\nhttps://t.me/Wallpoper_bot?startgroup=true"""


def get_message(data):
    try:
        chat_id = data['message']['chat']['id']
        text = data['message']['text']
        text = text.lower()
        username = data['message']['from']['username']
        #print(chat_id, text, username)
        return chat_id, text, username
    except:
        return False, False, False
      
def send_message(id, text):
    url = telegram_api+"/sendMessage"
    payload = {"chat_id": id, "text": text}
    res = post(url, json=payload)
    return res

def send_img(id, imglist):
    if len(imglist) == 0:
        send_message(id, "Couldn't get any wallpapers for your search!")
    url = telegram_api + '/sendMediaGroup'
    payload = {
        "chat_id": id,
        "media": imglist
    }
    res = post(url, json=payload)
    return res.text

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            msg = request.get_json()
            chat_id, txt, username = get_message(msg)
            if msg:
                if '/start' in txt:
                    print('Sending Welcome message')
                    send_message(chat_id, welcome.format(user = username))
                    return Response('ok', status=200)
                elif 'search' in txt:
                    new_txt = (txt.replace('search', '')).strip()
                    print('Searching:', new_txt)
                    walls = [p for p in get_images(new_txt)]
                    print('Wallpaper lists: ', len(walls))
                    first = walls[0]
                    second = walls[1]
                    print(first)
                    print('\n', second)
                    return Response('ok', status=200)
                else:
                    send_message(chat_id, 'Invalid request')
                    return Response('ok', status=200)
            else:
                return Response('ok', status=200)
        else:
            return "Bad request, only POST requests allowed"
    except Exception as e:
        return Response(f'Error: {e}', status=200)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, Response, request
from requests import get, post
import json
from wallpaper import get_images
from concurrent.futures import ThreadPoolExecutor, wait

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

def send_image(id, query, images):
    if images != None:
        try:
            print('Sending pics')
            url = telegram_api + '/sendMediaGroup'
            payload = {
                "chat_id": id,
                "media": images,
            }
            res = post(url, json=payload)
            return res
        except:
            print('Error oo')
            return None
    else:
        send_message(id, 'An error occurred')


def main(msg):
    chat_id, txt, username = get_message(msg)
    if txt:
        if '/start' in txt:
            print('Sending Welcome message')
            send_message(chat_id, welcome.format(user = username))
        elif 'search' in txt:
            new_txt = (txt.replace('search', '')).strip()
            print('Searching:', new_txt)
            send_image(chat_id, new_txt, [i for i in get_images(new_txt)])
            return Response('ok', status=200)
        else:
            return Response('ok', status=200)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        futures = []
        with ThreadPoolExecutor() as executor:
            for num in range(1,2):
                    futures.append(
                       executor.submit(main, msg)
                    )
        wait(futures)
    else:
        return "Bad command, you have doomed us"

if __name__ == '__main__':
    app.run(debug=True)
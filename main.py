from flask import Flask, Response, request
from requests import get, post
import json
from t import get_images
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
    if len(images) != 0:
        try:
            print('Sending pics')
            url = telegram_api + '/sendMediaGroup'
            payload = {
                "chat_id": id,
                "media": images,
                "caption": query
            }
            res = post(url, json=payload)
        except Exception as e:
            send_message(id, f"Error: {e}")
        finally:
            return True
    elif images == False:
        send_message(id, "An error occurred in the request.")
        return True
    else:
        send_message(id, f"Couldn't find any wallpapers on {query}")
        return True

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            msg = request.get_json()
            chat_id, txt, username = get_message(msg)
            if txt:
                if '/start' in txt:
                    print('Sending Welcome message')
                    send_message(chat_id, welcome.format(user = username))
                    return Response('ok', status=200)
                elif 'search' in txt:
                    new_txt = (txt.replace('search', '')).strip()
                    print('Searching:', new_txt)
                    #response = send_image(chat_id, new_txt, [i for i in get_images(new_txt)])
                    response = True
                    if response:
                        return Response('ok', status=200)
                    else:
                        return Response('Error in sending messages', status=500)
            else:
                return Response('ok', status=200)
        else:
            return "Bad request, only POST requests allowed"
    except Exception as e:
        return Response(f'Error: {e}', status=500)


if __name__ == '__main__':
    app.run(debug=True)

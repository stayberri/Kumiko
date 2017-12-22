import json
import requests
import urllib

with open('config.json', 'r') as f:
    config = json.load(f)


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


def request_image(type):
    url = f"https://api.weeb.sh/images/random?type={type}&hidden=false"
    r = requests.get(url,
                     headers={"Authorization": config['weeb-token']})
    j = r.json()
    return j['url']


def request_image_as_gif(type):
    url = f"https://api.weeb.sh/images/random?type={type}&hidden=false&filetype=gif"
    r = requests.get(url,
                     headers={"Authorization": config['weeb-token']})
    j = r.json()
    return j['url']


def request_image_as_png(type):
    url = f"https://api.weeb.sh/images/random?type={type}&hidden=false&filetype=png"
    r = requests.get(url,
                     headers={"Authorization": config['weeb-token']})
    j = r.json()
    return j['url']


def save_to_image(url, name):
    o = AppURLopener()
    d = o.open(url)
    data = d.read()
    with open("./images/" + name, "wb") as img:
        img.write(data)
        img.close()
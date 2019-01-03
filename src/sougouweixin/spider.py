import requests
from urllib.parse import urlencode
import json

base_url = "https://weixin.sogou.com/weixin?"

headers = {
    'Cookie': 'IPLOC=CN3701; SUID=BBA662DF3108990A000000005C2E1145; SUV=1546522949238309; ABTEST=0|1546522951|v1; SNUID=978D49F32C2955A1C30C76C12CB09D4F; weixinIndexVisited=1; sct=2; JSESSIONID=aaaVsxsp5VrHF5fKsh7Cw; ppinf=5|1546524354|1547733954|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo0NTolRTQlQjglOEQlRTUlQjAlODElRTUlODYlQkIlRTclOUElODQlRTQlQkElOTV8Y3J0OjEwOjE1NDY1MjQzNTR8cmVmbmljazo0NTolRTQlQjglOEQlRTUlQjAlODElRTUlODYlQkIlRTclOUElODQlRTQlQkElOTV8dXNlcmlkOjQ0Om85dDJsdUpTcmN6U080NmVUbWtNMjVLZkpQdmNAd2VpeGluLnNvaHUuY29tfA; pprdig=NK6ns9_-MaB-eee0A9jHmMDT6S1Q9SUC98FraCspDG-WlmzP-iP5ujajdcTIzThkUTRWdDIhzzNLhqFKXvk8xtChZ3szIl5cGIVlAEYCmRz9sdKTwmozdgIl-lC3dv2lxQSPRLHwZ_FIFnWTeeyqfM5726iZBZSuOThrpbAWmt4; sgid=26-38613879-AVwuFsFa8XkjFlq3VmBQPYE; ppmdig=154652435400000092a0138325d51708dbd08167b7843f66',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

keyword = "spring"


def get_proxy():
    try:
        response = requests.get("http://47.94.88.230/get")
    except ConnectionError as e:
        return get_proxy()
    if response.status_code == 200:
        proxy_string = response.text
    else:
        return get_proxy()
    proxys = json.loads(proxy_string)
    return proxys[0]


def get_html(url):
    try:
        response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            print(302)
    except ConnectionError as e:
        return get_html(url)


def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page,
    }
    querys = urlencode(data)
    url = base_url + querys
    content = get_html(url)
    return content


def main():
    for page in range(1, 101):
        print(page)
        html = get_index(keyword, page)


if __name__ == '__main__':
    print(get_proxy())

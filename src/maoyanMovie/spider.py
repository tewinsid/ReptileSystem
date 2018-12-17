import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool


def get_on_page(url):
    try:
        header = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
        }
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(content):
    regex = '<dd>.*?board-index-.*?">(\d+)</i>.*?' \
            'data-src="(.*?)".*?name".*?">(.*?)</a>.*?star">(.*?)</p>.*?' \
            'releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?' \
            'fraction">(.*?)</i>.*?</dd>'
    pattern = re.compile(regex, re.S)
    items = re.findall(pattern, content)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'name': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'source': item[5] + item[6]
        }


def write_to_file(content):
    with open('/home/grape/Documents/temp/result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    if offset == 0:
        url = url[:-9]
    print(url)
    html = get_on_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 10 for i in range(10)])

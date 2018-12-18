import requests
import re
import json
from urllib.parse import urlencode
from bs4 import BeautifulSoup

from requests import RequestException


def get_page_index(offset, keyword):
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    }
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    log(url)
    try:
        response = requests.get(url, headers=header)
        print(response)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        log('请求索引出错')
        return None


def parse_page_index(html):
    content = json.loads(html)
    if content and 'data' in content.keys():
        for item in content.get('data'):
            yield item.get('article_url')


def get_page_detail(url):
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        log('请求detail也出错')
        return None


def parse_page_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    regex = 'gallery: JSON.parse{(.*?)}.*?siblingList'
    pattern = re.compile(regex, re.S)
    json_string = re.search(pattern, html)
    if json_string:
        print(json_string.group(1))
    # result = json.loads(json_string)
    # yield result.get('pgc-image')


def log(*args, **kwargs):
    print('log', *args, **kwargs)


def main():
    html = get_page_index(0, '街拍')
    for url in parse_page_index(html):
        if url:
            detail = get_page_detail(url)
            parse_page_detail(detail)


if __name__ == '__main__':
    main()

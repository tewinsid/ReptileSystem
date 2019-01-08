import os
from _md5 import md5

import requests
import re
import json
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from toutiaoJiePai.config import *
from requests import RequestException
import pymongo
from multiprocessing import Pool

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


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
        'cur_tab': 3,
        'from': 'gallery',
        'pd': ''
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url, headers=header)
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


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    regex = 'gallery: JSON.parse((.*)),.*?siblingList'
    pattern = re.compile(regex, re.S)
    json_string = re.search(pattern, html)
    if json_string:
        json_result = json_string.group(1)[1:-1]
        data = json.loads(eval(json_result))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:
                download_image(image)
            return {
                'title': title,
                'url': url,
                'images': images
            }


def save_to_mongo(result):
    log(result)
    if db[MONGO_TABLE].insert(result):
        log('save_to_mongo', '存储ｍｏｎｇｏ成功', result)
        return True
    return False


def log(*args, **kwargs):
    print('log', *args, **kwargs)


def download_image(url):
    log('download_image', '正在下载', url)
    header = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            # response.content返回二进制
            save_image(response.content)
        else:
            return None
    except RequestException:
        log('请求图片出错')
        return None


def save_image(content):
    file_path = "{0}/{1}.{2}".format(os.getcwd() + '/image', md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)


def main(offset):
    html = get_page_index(offset, KEYWORD)
    for url in parse_page_index(html):
        if url:
            detail = get_page_detail(url)
            if detail:
                result = parse_page_detail(detail, url)
                save_to_mongo(result)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 20 for i in range(RANGE_START, RANGE_END)])

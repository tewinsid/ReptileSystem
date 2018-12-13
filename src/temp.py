import requests
import re
from bs4 import BeautifulSoup


def test():
    url = 'https://book.douban.com/'

    headers = {
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    }
    content = requests.get(url, headers=headers).text
    content = re.sub('\s', '', content)
    i = 0
    index = 0
    while i < len(content):
        index = match(content[i:i + 10000], index)
        i = i + 10000


def match(content, index):
    regex = '<li.*?cover.*?href="(.*?)".*?title="(.*?)".*?more-meta.*?author">(.*?)</span>.*?year">(.*?)</span>.*?</li>'
    pattern = re.compile(regex, re.S)
    results = re.findall(pattern, content)
    for result in results:
        url, name, author, date = result
        index = index + 1
        print(index, url, name, author, date)
    return index


def main():
    url = 'http://www.baidu.com'

    headers = {
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    }
    content = requests.get(url, headers=headers).text
    content = re.sub('\s', '', content)
    print(len(content))
    content = content[:20000]
    soup = BeautifulSoup(content, 'lxml')
    # 格式化代码　自动补全
    print(soup.prettify())
    print(soup.title.string)


if __name__ == '__main__':
    main()

import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from taobaoPicture.config import *
import pymongo

# browser = webdriver.Chrome()
browser = webdriver.PhantomJS(SERVICE_ARG)
browser.set_window_size(1366, 768)
wait = WebDriverWait(browser, 10)

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def search():
    log('search')
    browser.get('https://www.taobao.com/')
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
        )
        input.send_keys('美食')
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total")))
        get_products()
        return total.text
    except TimeoutException:
        return search()


def next_page(page_number):
    log('next_page')
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
        confirm = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")))
        input.clear()
        input.send_keys(page_number)
        confirm.click()

        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)


def get_products():
    log('get_products')
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-itemlist .items .item")))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price strong').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()

        }
        save_to_mongo(product)


def save_to_mongo(result):
    log(result)
    try:
        if db[MONGO_TABLE].insert(result):
            log('save_to_mongo', 'success', result)
    except Exception:
        log('save_to_mongo', 'faile', 'result')


def main():
    total = search()
    total = int(re.compile('(\d+)').search(total).group(0))
    log(total)
    for i in range(2, total + 1):
        next_page(i)


def log(*args, **kwargs):
    print('log', *args, **kwargs)


if __name__ == '__main__':
    main()
    browser.close()

# 首先链接目标站点
# 目标站点数据展示形式，一般用url参数处理页码，
# 对于比较复杂页面使用selenium记性模拟请求，这时需要处理输入和点击等时间，以及翻页操作
# 数据都能获取到的情况下，解析界面，找到需要信息

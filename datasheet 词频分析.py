# 6:39PM, Apr 3th, 2018 @ HDU_Wireless
# 爬取 TI 公司的芯片手册，统计高频词汇，储存为 Excel 表格
# URL  (TPS5430)
# http://www.ti.com/product/TPS5430/datasheet

# TI 的 online datasheet 网页是动态网页
# 观察源代码发现，所有的动态加载链接都在 data-val 字段后

import re
import xlwt
import requests
from lxml import etree

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

def wf_analyse(sentence):
    new_words = []
    words = sentence.split()
    i = 0
    for word in words:
        word = word.strip(',.').lower()
        if word.isalpha() == True:
            new_words.append(word)
    words_set = set(new_words)
    print(words_set)
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('Sheet')
    for word in words_set:
        count = new_words.count(word)
        # sheet.write(#行，#列，#内容)
        i += 1
        sheet.write(i, 0, word)
        sheet.write(i, 1, count)
    book.save('E:\AllPrj\PyCharmPrj\py-crawler\TI-Datasheet-Crawler\词频分析.xls')

def get_infos(links):
    sentence = ''
    i = 0
    for link in links:
        i += 1
        print(link, i)
        res = requests.get(link, headers=headers)
        selector = etree.HTML(res.text)
        contents = selector.xpath('//div[@class="subsection"]')
        for content in contents:
            words = content.xpath('p')
            for word in words:
                word = word.xpath('text()')
                for item in word:
                    sentence += item
    wf_analyse(sentence)

# 获取动态加载链接
def get_urls(url):
    res = requests.get(url, headers=headers)
    links = re.findall('data-val.*?href="(.*?)"', res.text, re.S)
    get_infos(links)

def main():
    url = 'http://www.ti.com/product/TPS5430/datasheet'
    get_urls(url)

if __name__ == '__main__':
    main()

import requests
import traceback
import lxml
import json
import re
from bs4 import BeautifulSoup
from bs4 import element
import threading

base_url = r'http://jib.xywy.com/il_sii/' # 爬取网站的基地址
headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
data_post = {} # post传入参数
data_get = {} # get传入参数
cookies = ''
session = requests.session()
file = open('data.json','a+',encoding='utf-8')
error = open('error2.json','a+',encoding='utf-8')
def fetch_html(postfix=''):
    target_url = base_url + postfix
    #response_session = session.get(target_url,params=data_get,cookies=cookies,headers=headers)
    #response = requests.post(target_url,data=data_post,cookies=cookies,headers=headers)
    response = requests.get(target_url,params=data_get,cookies=cookies,headers=headers)
    if response.status_code==200:
        return response.text
    else:
        print(target_url,'Error',response.status_code)
        return ''

def parse_soup(soup):
    selector= '' # 拷贝选择子
    #cons = soup.find_all(selector)
    res = soup.find(selector)




class WebCrawler(threading.Thread):
    def __init__(self,begin,end=-1):
        super().__init__()
        self.begin = begin
        if end == -1:
            self.end = begin+1
        else:
            self.end = end

    def trip_white(self,input_str:str):
        return input_str.replace('\xa0', '').replace('\n', '').replace('\r', '')\
            .replace('\t', '').replace('    ','').strip()

    def get_html_text(self,url):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return ''

    def fetch_and_parse_gaishu(self,tartget_url):
        res = self.get_html_text(tartget_url)
        soup = BeautifulSoup(res,'lxml')
        gaishu_data = {}

        # 疾病名称选择子
        selector = 'body > div.wrap.mt5 > div'
        res = soup.select(selector)[0]
        gaishu_data['ill_name'] = res.get_text()

        # 医保疾病
        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div:nth-child(2) > p:nth-child(2) > span.fl.txt-right'
        res = soup.select(selector)[0]
        gaishu_data['insurance'] = self.trip_white(res.get_text())

        # 患病比例
        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div:nth-child(2) > p:nth-child(3) > span.fl.txt-right'
        res = soup.select(selector)[0]
        gaishu_data['mobidity'] = self.trip_white(res.get_text())

        # 易感人群
        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div:nth-child(2) > p:nth-child(4) > span.fl.txt-right'
        res = soup.select(selector)[0]
        gaishu_data['susceptible'] = self.trip_white(res.get_text())

        # 传染方式
        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div:nth-child(2) > p:nth-child(5) > span.fl.txt-right'
        res = soup.select(selector)[0]
        gaishu_data['spread'] = self.trip_white(res.get_text())

        # 并发症
        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div:nth-child(2) > p:nth-child(6) > span.fl.txt-right'
        res = soup.select(selector)[0]
        neopathy = []
        for item in res:
            if type(item) is element.Tag:
                neopathy.append(item.get_text())
        gaishu_data['neopathy'] = neopathy

        # 就诊科室
        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div:nth-child(3) > p:nth-child(2) > span.fl.txt-right'
        res = soup.select(selector)[0]
        gaishu_data['department'] = [i for i in list(res.get_text().split(' ')) if len(i)>0]

        # 治疗方式
        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div:nth-child(3) > p:nth-child(3) > span.fl.txt-right'
        res = soup.select(selector)[0]
        gaishu_data['treatment'] = [i for i in list(res.get_text().split(' ')) if len(i)>0]

        # 治疗周期
        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div:nth-child(3) > p:nth-child(4) > span.fl.txt-right'
        res = soup.select(selector)[0]
        gaishu_data['period'] = self.trip_white(res.get_text())

        # 治愈率
        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div:nth-child(3) > p:nth-child(5) > span.fl.txt-right'
        res = soup.select(selector)[0]
        gaishu_data['cure_ratio'] = self.trip_white(res.get_text())

        # 常用药品
        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div:nth-child(3) > p:nth-child(6) > span.fl.txt-right'
        res = soup.select(selector)[0]
        drugs = []
        for item in res:
            if type(item) is element.Tag:
                drugs.append(item.get_text())
        gaishu_data['drugs'] = drugs

        # 治疗费用
        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div:nth-child(3) > p:nth-child(7) > span.fl.txt-right'
        if len(soup.select(selector)) == 0: # 部分疾病没有常用药品
            selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div:nth-child(3) > p:nth-child(6) > span.fl.txt-right'
        res = soup.select(selector)[0]
        gaishu_data['cost'] = self.trip_white(res.get_text())

        # 温馨提示
        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div:nth-child(4) > p'
        res = soup.select(selector)[0]
        gaishu_data['suggestion'] = self.trip_white(res.get_text())

        # 简介选择子
        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div.jib-articl-con.jib-lh-articl > p'
        res = soup.select(selector)[0]
        gaishu_data['desc'] = self.trip_white(res.get_text())

        return gaishu_data

    def fetch_and_parse_standard(self,target_url):
        res = self.get_html_text(target_url)
        soup = BeautifulSoup(res,'lxml')
        # 标准提取，从文章栏中提取出p元素内容并去除空白符

        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14.jib-lh-articl'
        res = soup.select(selector)[0]
        return ''.join([self.trip_white(i.get_text()) for i in res if i.name == 'p'])

    def fetch_and_parse_treat(self,target_url):
        res = self.get_html_text(target_url)
        soup = BeautifulSoup(res,'lxml')
        # 治疗方案
        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14 > div.jib-lh-articl'
        res = soup.select(selector)[0]
        return ''.join([self.trip_white(i.get_text()) for i in res if i.name == 'p'])

    def fetch_and_parse_neopathy(self,target_url):
        res = self.get_html_text(target_url)
        soup = BeautifulSoup(res,'lxml')
        # 并发症
        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14.jib-lh-articl > span'
        res = soup.select(selector)[0]
        return [self.trip_white(i.get_text()) for i in res if i.name == 'a']

    def fetch_and_parse_food(self,target_url):
        res = self.get_html_text(target_url)
        soup = BeautifulSoup(res, 'lxml')
        data_food = {}
        # 食物宜忌
        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14.jib-lh-articl > div > div.panels.mt10 > div.diet-item.none.clearfix > div.diet-good.clearfix > div.fl.diet-good-txt'
        res = soup.select(selector)[0]
        data_food['宜食'] = self.trip_white(res.get_text())

        selector = 'body > div.wrap.mt10.clearfix.graydeep > div.main-sub.fl > div.jib-janj.bor.clearfix > div.jib-articl.fr.f14.jib-lh-articl > div > div.panels.mt10 > div:nth-child(3) > div.diet-good.clearfix > div.fl.diet-good-txt'
        res = soup.select(selector)[0]
        data_food['忌食'] = self.trip_white(res.get_text())

        return data_food

    def run(self) -> None:
        ill_data = {}
        for page_num in range(self.begin,self.end):
            try:
                ill_data['gaishu'] = self.fetch_and_parse_gaishu(base_url+f'gaishu/{page_num}.htm') # 简介
                ill_data['cause'] = self.fetch_and_parse_standard(base_url+f'cause/{page_num}.htm') # 病因
                ill_data['prevent'] = self.fetch_and_parse_standard(base_url+f'prevent/{page_num}.htm') # 预防
                ill_data['neopathy'] = self.fetch_and_parse_neopathy(base_url+f'neopathy/{page_num}.htm') # 并发症
                ill_data['symptom'] = self.fetch_and_parse_standard(base_url+f'symptom/{page_num}.htm') # 症状
                ill_data['inspect'] = self.fetch_and_parse_standard(base_url+f'inspect/{page_num}.htm') # 检查
                ill_data['diagnosis'] = self.fetch_and_parse_standard(base_url+f'diagnosis/{page_num}.htm') # 并发症
                ill_data['treat'] = self.fetch_and_parse_treat(base_url+f'treat/{page_num}.htm') # 治疗
                ill_data['nursing'] = self.fetch_and_parse_standard(base_url+f'nursing/{page_num}.htm') # 护理
                ill_data['food'] = self.fetch_and_parse_food(base_url+f'food/{page_num}.htm') # 饮食
                ans = json.dumps(ill_data,ensure_ascii=False)
                print(ans,file=file)
                print(f'{page_num} OK')
            except Exception as e:
                traceback.print_exc()
                print(e,f'[ Error at {page_num}.htm]',file=error)
                print(f'{page_num} Failed')
            file.flush()
def craw():
    thread1 = WebCrawler(10000,10500)
    thread2 = WebCrawler(10500,11000)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

def errorfix():
    file = open('error.json','r',encoding='utf8')
    with open('error_backup.json','w',encoding='utf8') as f:
        for line in file:
            if not line.startswith('list index out of range'):
                f.write(line)

# thread_test = WebCrawler(9)
# thread_test.start()
# thread_test.join()
def craw2():
    error_backup = open('error_backup.json','r',encoding='utf8')
    pattern = re.compile(r'(\d+).htm')
    for line in error_backup:
        page = pattern.findall(line)
        try:
            thread_test = WebCrawler(int(page[0]))
            thread_test.start()
            thread_test.join()
        except:
            traceback.print_exc()
    error_backup.close()
if __name__ == '__main__':
    craw2()
"""Data format:
gaishu                  概述
        ill_name        疾病名称
        insurance       是否是医保疾病
        mobidity        患病比例
        susceptible     易感人群
        spread          传播方式
        neopathy        并发症名称
        department      科室
        treatment       治疗方式
        period          治疗周期
        cure_ratio      治愈率
        drugs           药品
        cost            花销
        suggestion      相关提示
        desc            疾病描述
cause                   病因
prevent                 预防方法
neopathy                并发症详述
symptom                 症状
inspect                 检查项目
diagnosis               诊断鉴别
treat                   治疗方式
nursing                 护理
food                    食物宜忌
        宜食
        忌食
"""
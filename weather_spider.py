import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import argparse


def wether_spider(city,year):
    print('开始爬取{}年天气数据'.format(year))
    # month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11','12']
    month_list = ['01', '02']
    date_list, wether, temperature, wind_power = [], [], [], []
    for month in month_list:
        url = 'http://www.tianqihoubao.com/lishi/{0}/month/{1}{2}.html'.format(city, year, month)
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table',class_='b')
        tr_list = table.find_all('tr')

        for tr in tr_list[1:]:
            # 获得每天的数据列表
            td_list = tr.find_all('td')
            rq = td_list[0].text.strip()  # 日期
            tqzk = re.sub(r'\s*', '', td_list[1].text.strip())  # 天气状况
            qw = re.sub(r'\s*', '', td_list[2].text.strip())  # 气温
            fx = re.sub(r'\s*', '', td_list[3].text.strip())  # 风力风向
            date_list.append(rq)
            wether.append(tqzk)
            temperature.append(qw)
            wind_power.append(fx)
        print('{}月天气数据爬取完毕'.format(month))
    wether_data = pd.DataFrame({'日期':date_list,'天气情况':wether,'气温':temperature,'风力风向':wind_power})
    wether_data.to_csv('data/{}_{}_weather.csv'.format(city,year),encoding='gbk',index=False)

if __name__ == '__main__':
    date = time.localtime()  # 获取当前时间
    parser = argparse.ArgumentParser(description='weather')
    parser.add_argument('--city', type=str, default='taiyuan', required=False)
    parser.add_argument('--start_year', type=int, default=2022, required=False)
    parser.add_argument('--end_year', type=int, default=date.tm_year, required=False)
    args = parser.parse_args()
    for year in range(args.start_year,args.end_year+1):
        wether_spider(args.city,year)
        print('{}年数据爬取完毕，并保存'.format(args.city,year))

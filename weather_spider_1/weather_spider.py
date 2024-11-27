# 日期，最高气温，最高气温，天气，风向
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import pypinyin
import argparse
import time


def Pinyin(city):
    b = pypinyin.pinyin(city, style=pypinyin.NORMAL)
    city_pinyin = ''
    for i in b:
        city_pinyin += ''.join(i)
    return city_pinyin


def weather_spider(city, year):
    city_pinyin = Pinyin(city)
    # url = 'http://lishi.tianqi.com/taiyuan/202310.html'
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19"}
    # month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    month_list = ['01', '02']
    date_list, max_temperature, min_etemprature, weather, wind_power = [], [], [], [], []
    for month in month_list:
        url = 'http://lishi.tianqi.com/{}/{}{}.html'.format(city_pinyin, year, month)
        urr = urllib.request.Request(url, headers=headers)
        # response =urllib.request.urlopen(urr).read()
        response = urllib.request.urlopen(urr).read().decode()

        soup = BeautifulSoup(response, "lxml")
        tqtongji1 = soup.find("div", {"class": "tian_three"})
        all_url = tqtongji1.find_all('li')

        for i in all_url:
            date = i.find('div', class_='th200')
            date_list.append(date.get_text())
            j = i.find_all('div', class_='th140')
            if len(j) >= 2:
                max_temperature.append(j[0].get_text())
                min_etemprature.append(j[1].get_text())
                weather.append(j[2].get_text())
                wind_power.append(j[3].get_text())
        print('{}月天气爬虫完毕'.format(month))
    weather_data = pd.DataFrame(
        {'date': date_list, 'max_temperature': max_temperature, 'min_etemprature': min_etemprature, 'weather': weather,
         'wind_power': wind_power})
    weather_data.to_csv('data/{}_{}_weather.csv'.format(year, city), encoding='gbk', index=False)
    print('{}年天气数据爬虫完毕，并已保存'.format(year))


if __name__ == '__main__':
    date = time.localtime()  # 获取当前时间
    parser = argparse.ArgumentParser(description='weather')
    parser.add_argument('--city', type=str, default='太原', required=False)
    parser.add_argument('--start_year', type=int, default=2022, required=False)
    parser.add_argument('--end_year', type=int, default=date.tm_year, required=False)
    args = parser.parse_args()
    for year in range(args.start_year, args.end_year + 1):
        print('开始爬取{}年天气数据'.format(year))
        weather_spider(args.city, year)

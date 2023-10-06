import requests
from bs4 import BeautifulSoup
import datetime as dt
import csv
import ray
import time

# 뉴스 제목 본문 등 크롤링하는 함수
def get_news(URL) :

  res = requests.get(URL)
  soup = BeautifulSoup(res.text, 'html.parser')

  title = soup.select_one('h2#title_area > span').text
  content = soup.select_one('article#dic_area').text.strip().replace('\n',' ')
  # date = soup.select_one('span._ARTICLE_DATE_TIME').text # 이거보다
  date = soup.select_one('span._ARTICLE_DATE_TIME')['data-date-time'] # 이게 날짜형태로 변환할 수 있어서 더 좋음
  media = soup.select_one('a.media_end_head_top_logo > img')['title']

  return (title, date, media, content, URL)



# 키워드, 날짜 입력하면 그 기간동안 모든 뉴스 리스트 뽑아서 csv로 저장하는 함수 
@ray.remote
def get_news_list(keyword, startdate, enddate) : 

  file = open("news_tesla_ray.csv",mode="w",encoding="utf-8",newline="")
  writer = csv.writer(file)

  headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    ,'Referer':'https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%ED%85%8C%EC%8A%AC%EB%9D%BC&sort=1&photo=0&field=0&pd=3&ds=2023.09.21&de=2023.09.21&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:from20230921to20230921,a:all&start=91'
  }
  startdate = dt.datetime.strptime(startdate, '%Y.%m.%d')
  enddate = dt.datetime.strptime(enddate, '%Y.%m.%d')

  for d in range(0, (enddate - startdate).days + 1) :
    nowdate = startdate + dt.timedelta(days=d)
    # print(nowdate)
    nowdate = str(nowdate.strftime('%Y.%m.%d'))
    page = 1

    while True :
      start = (page-1)*10 + 1
      URL = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=1&photo=0&field=0&pd=3&ds={}&de={}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:dd,p:from{}to{},a:all&start={}'.format(keyword, nowdate, nowdate, nowdate.replace('.',''), nowdate.replace('.',''),start)
      res = requests.get(URL, headers=headers)
      soup = BeautifulSoup(res.text, 'html.parser') 

      if soup.select('ul.list_news') == [] :
        break

      for li in soup.select('ul.list_news > li') :
        if len(li.select('div.info_group > a')) == 2 :
          print(li.select('div.info_group > a')[1]['href'])
          writer.writerow(get_news(li.select('div.info_group > a')[1]['href']))
      
      page += 1

  file.close()


start_time = time.time()

tesla = get_news_list.remote('테슬라', '2022.09.29', '2022.9.30')
result = ray.get(tesla)

ray.shutdown()

end_time = time.time()

print('소요시간 : ', end_time - start_time)   # 소요시간 :  101.68625545501709
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

for date in range(20230801,20230803) : 

  for page in range(1,2) :
    params = {'mode':'LPOD', 'mid':'sec', 'oid':'001', 'date':date, 'page':page}
    yeonhap = requests.get('https://news.naver.com/main/list.naver', headers=headers, params=params)
    yh = BeautifulSoup(yeonhap.text, 'html.parser')

    if sis.select_one('div.paging > strong') == before_sis.select_one('div.paging > strong') :
      break

    for dt in yh.select('div.list_body li dt') :

      if dt.attrs == {} :
          print(dt.find('a').text.strip())
          # print(dt.find('a').attrs['href'].strip())
          yeonhap2 = requests.get(dt.find('a').attrs['href'].strip())
          yh2 = BeautifulSoup(yeonhap2.text, 'html.parser')

          if yh2.find('article') != None :
            print(yh2.find('article').text.replace('\n', ' ').strip(),'\n')
          elif yh2.find('div', id='newsEndContents') != None :
            print(yh2.find('div', id='newsEndContents').text.replace('\n', ' ').strip(),'\n')
          elif yh2.find('div', id='articeBody') != None :
            print(yh2.find('div', id='articeBody').text.replace('\n', ' ').strip(),'\n')
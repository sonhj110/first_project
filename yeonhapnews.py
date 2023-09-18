import requests
from bs4 import BeautifulSoup
import re 
import json

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

def count_react(dic) :
  reactNum = 0
  for emo in dic :
    reactNum = reactNum + int(emo['count'])
  return reactNum

def get_react(link) :
  result = re.search('{.+}', link.text)
  return json.loads(result.group())

for date in range(20230801,20230803) :

  for page in range(3,10) :
    params = {'mode':'LPOD', 'mid':'sec', 'oid':'001', 'date':date, 'page':page}
    yeonhap = requests.get('https://news.naver.com/main/list.naver', headers=headers, params=params)
    yh = BeautifulSoup(yeonhap.text, 'html.parser')

    for dt in yh.select('div.list_body li dt') :

      if dt.attrs == {} :
          print(dt.find('a').text.strip(), yh.select_one('div.list_body li > dl > dd > span.date').text)  # 기사제목, 날짜
          # print(dt.find('a').attrs['href'].strip())   # 뉴스링크
          result = re.search('[0-9]{10}', dt.find('a').attrs['href'])
          aid = result.group()
          yeonhap2 = requests.get(dt.find('a').attrs['href'].strip())
          yh2 = BeautifulSoup(yeonhap2.text, 'html.parser')


          if yh2.find('article') != None :   # 일반뉴스
            print(yh2.find('article').text.replace('\n', ' ').strip(),'\n')


          elif yh2.find('div', id='newsEndContents') != None :   # 스포츠
            print(yh2.find('div', id='newsEndContents').text.replace('\n', ' ').strip())

            cid = yh2.find('div', attrs={'data-ccounttype':'period'}).attrs['data-cid']
            params = {
            'q': 'SPORTS[ne_001_' + aid + ']|JOURNALIST[' + cid + '(period)]|SPORTS_MAIN[ne_001_' + aid + ']'
            }
            res = requests.get('https://sports.like.naver.com/v1/search/contents', headers=headers, params=params)
            yhdic = get_react(res)

            print('반응수 :', count_react(yhdic['contents'][0]['reactions']),'\n')


          elif yh2.find('div', id='articeBody') != None :   # 연예
            # print('카테고리 :', yh2.select_one('em.guide_categorization_item').text)
            print(yh2.find('div', id='articeBody').text.replace('\n', ' ').strip())

            cid = yh2.find('div', attrs={'data-ccounttype':'period'}).attrs['data-cid']
            params = {
              'q': 'ENTERTAIN[ne_001_' + aid + ']|JOURNALIST[' + cid + '(period)]|ENTERTAIN_MAIN[ne_001_' + aid + ']'
            }
            res = requests.get('https://news.like.naver.com/v1/search/contents', headers=headers, params=params)
            yhdic = get_react(res)

            print('반응수 :', count_react(yhdic['contents'][0]['reactions']),'\n')

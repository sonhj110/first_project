import requests
from bs4 import BeautifulSoup
import re 
import json

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

def modify(body) :
  # body = BeautifulSoup(re.sub('<em class="img_desc">((?!<\/em>).)*<\/em>', '', str(body))).text
  result = re.search('(.|\n)*(?=[^a-zA-Z0-9][a-zA-Z0-9]+@[a-zA-Z]+\.(com|kr|co.kr))', body.text)
  body = result.group()
  body = re.sub('\([가-힣]+\=연합뉴스\) [가-힣]{2,4} (기자|특파원|통신원) \=', '', body) 
  return body.replace('\n', ' ').strip()

def count_react(dic) :
  reactNum = 0
  for emo in dic :
    reactNum = reactNum + int(emo['count'])
  return print('반응수 :', reactNum, '\n')

def get_react(link) :
  result = re.search('{.+}', link.text)
  return json.loads(result.group())



for date in range(20230801,20230803) :

  for page in range(1,3) :
    params = {'mode':'LPOD', 'mid':'sec', 'oid':'001', 'date':date, 'page':page}
    yeonhap = requests.get('https://news.naver.com/main/list.naver', headers=headers, params=params)
    yh = BeautifulSoup(yeonhap.text, 'html.parser')

    for dt in yh.select('div.list_body li dt') :

      if dt.attrs == {} :
          print(dt.find('a').text.strip(), yh.select_one('div.list_body li > dl > dd > span.date').text.split(' ')[0])  # 기사제목, 날짜
          print(dt.find('a').attrs['href'].strip())   # 뉴스링크
          result = re.search('[0-9]{10}', dt.find('a').attrs['href'])
          aid = result.group()
          yeonhap2 = requests.get(dt.find('a').attrs['href'].strip())
          yh2 = BeautifulSoup(yeonhap2.text, 'html.parser')


          if yh2.find('article') != None :   # 일반뉴스
            # print(yh2.find('article').text.replace('\n', ' ').strip())
            print(yh2.select_one('em.media_end_categorize_item').text,'섹션')
            print(modify(yh2.find('article')))

            if yh2.find('div', attrs={'data-ccounttype':'period'}) != None :
              cid = yh2.find('div', attrs={'data-ccounttype':'period'}).attrs['data-cid']
              params = {
                'q': 'JOURNALIST[' + cid + '(period)]|NEWS[ne_001_' + aid + ']'
                }
              res = requests.get('https://news.like.naver.com/v1/search/contents', headers=headers, params=params)
              yhdic = get_react(res)
              count_react(yhdic['contents'][1]['reactions'])

            else :
              params = {'q': 'NEWS[ne_001_' + aid + ']'}
              res = requests.get('https://news.like.naver.com/v1/search/contents', headers=headers, params=params)
              yhdic = get_react(res)
              count_react(yhdic['contents'][0]['reactions'])



          elif yh2.find('div', id='newsEndContents') != None :   # 스포츠
            print('스포츠 섹션')
            # print(yh2.find('div', id='newsEndContents').text.replace('\n', ' ').strip())
            print(modify(yh2.find('div', id='newsEndContents')))
            print('스포츠 섹션')

            cid = yh2.find('div', attrs={'data-ccounttype':'period'}).attrs['data-cid']
            params = {
              'q': 'SPORTS[ne_001_' + aid + ']|JOURNALIST[' + cid + '(period)]|SPORTS_MAIN[ne_001_' + aid + ']'
              }
            res = requests.get('https://sports.like.naver.com/v1/search/contents', headers=headers, params=params)
            yhdic = get_react(res)

            count_react(yhdic['contents'][0]['reactions'])


          elif yh2.find('div', id='articeBody') != None :   # 연예
            print('연예 섹션')
            # print(yh2.find('div', id='articeBody').text.replace('\n', ' ').strip())
            print(modify(yh2.find('div', id='articeBody')))

            cid = yh2.find('div', attrs={'data-ccounttype':'period'}).attrs['data-cid']
            params = {
                'q': 'ENTERTAIN[ne_001_' + aid + ']|JOURNALIST[' + cid + '(period)]|ENTERTAIN_MAIN[ne_001_' + aid + ']'
              }
            res = requests.get('https://news.like.naver.com/v1/search/contents', headers=headers, params=params)
            yhdic = get_react(res)

            count_react(yhdic['contents'][0]['reactions'])

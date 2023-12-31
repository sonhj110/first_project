import requests
from bs4 import BeautifulSoup
import re
import json
import csv
file = open("news.csv",mode="w",encoding="utf-8",newline="")
writer = csv.writer(file)

writer.writerow(['제목','날짜','분류','본문','반응수'])

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

def modify(body) :
  # body = BeautifulSoup(re.sub('<em class="img_desc">((?!<\/em>).)*<\/em>', '', str(body))).text
  try :
    del_email = re.search('(.|\n)*(?=[^a-zA-Z0-9][a-zA-Z0-9]+@[a-zA-Z]+\.(com|kr|co.kr))', body)
    body = del_email.group()
  except :
    pass
  finally :
    body = re.sub('\([가-힣]+\=연합뉴스\)', '', body)
    body = re.sub('[가-힣]{2,4} (기자|특파원|통신원) \=', '', body)
  return body.replace('\n', ' ').strip()

def count_react(dic) :
  reactNum = 0
  for emo in dic :
    reactNum = reactNum + int(emo['count'])
  return reactNum

# def get_react(link) :
#   reactLink = re.search('{.+}', link.text)  # 이거 안해도 됨 params값 q만 남기니까 이상한 문자 다 지워짐
#   return json.loads(reactLink.group())


for date in range(20230801,20230832) :

  for page in range(1,1000) :
    yeonhap = requests.get(f'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=001&date={date}&page={page}', headers=headers)
    yh = BeautifulSoup(yeonhap.text, 'html.parser')

    if int(yh.select_one('div.paging > strong').text) != page :
      break

    for dt in yh.select('div.list_body li dt') :

      if dt.attrs == {} :
          temp = []
          temp.append(dt.find('a').text.strip())
          temp.append(date)

          result = re.search('[0-9]{10}', dt.find('a').attrs['href'])
          aid = result.group()
          print(dt.find('a').attrs['href'].strip())    # 기사링크 출력
          yeonhap2 = requests.get(dt.find('a').attrs['href'].strip())
          yh2 = BeautifulSoup(yeonhap2.text, 'html.parser')


          if yh2.find('article') != None :   # 일반뉴스

            try :
              temp.append(yh2.select_one('em.media_end_categorize_item').text)
            except :
              temp.append('없음')

            temp.append(modify(yh2.find('article').text))

            if yh2.find('div', attrs={'data-ccounttype':'period'}) != None :
              cid = yh2.find('div', attrs={'data-ccounttype':'period'}).attrs['data-cid']
              params = {'q': f'JOURNALIST[{cid}(period)]|NEWS[ne_001_{aid}]'}
              res = requests.get('https://news.like.naver.com/v1/search/contents', headers=headers, params=params)
              yhdic = json.loads(res.text)
              temp.append(count_react(yhdic['contents'][1]['reactions']))

            else :
              params = {'q': f'NEWS[ne_001_{aid}]'}
              res = requests.get('https://news.like.naver.com/v1/search/contents', headers=headers, params=params)
              yhdic = json.loads(res.text)
              temp.append(count_react(yhdic['contents'][0]['reactions']))


          elif yh2.find('div', id='newsEndContents') != None :   # 스포츠
            temp.append('스포츠')
            temp.append(modify(yh2.find('div', id='newsEndContents').text))

            if yh2.find('div', attrs={'data-ccounttype' : 'period'}) != None :
              cid = yh2.find('div', attrs={'data-ccounttype':'period'}).attrs['data-cid']
              params = {'q': f'SPORTS[ne_001_{aid}]|JOURNALIST[{cid}(period)]|SPORTS_MAIN[ne_001_{aid}]'}
            
            else :
              params = {'q': f'SPORTS[ne_001_{aid}]|SPORTS_MAIN[ne_001_{aid}]'}

            res = requests.get('https://sports.like.naver.com/v1/search/contents', headers=headers, params=params)
            yhdic = json.loads(res.text)
            temp.append(count_react(yhdic['contents'][0]['reactions']))


          elif yh2.find('div', id='articeBody') != None :   # 연예
            temp.append('연예')
            temp.append(modify(yh2.find('div', id='articeBody').text))

            if yh2.find('div', attrs={'data-ccounttype' : 'period'}) != None :
              cid = yh2.find('div', attrs={'data-ccounttype':'period'}).attrs['data-cid']
              params = {'q': f'ENTERTAIN[ne_001_{aid}]|JOURNALIST[{cid}(period)]|ENTERTAIN_MAIN[ne_001_{aid}]'}
            
            else :
              params = {'q': f'ENTERTAIN[ne_001_{aid}]|ENTERTAIN_MAIN[ne_001_{aid}]'}              
            res = requests.get('https://news.like.naver.com/v1/search/contents', headers=headers, params=params)
            yhdic = json.loads(res.text)
            temp.append(count_react(yhdic['contents'][0]['reactions']))

          print(temp)
          writer.writerow(temp)
    

file.close()
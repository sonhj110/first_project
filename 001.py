import requests
import re
from bs4 import BeautifulSoup
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}


for page in range(2,5) :

  params = {
      'code' : '005930'
    ,'page' : page
  }
  res = requests.get('https://finance.naver.com/item/sise_day.naver', headers=headers, params=params)
  sams = BeautifulSoup(res.text, 'html.parser')

  for tr in sams.select('table.type2 > tr') :

    if tr.attrs != {} :
      # print(tr.select('td')[0])
      if re.match('2023.08.+', tr.select('td')[0].text) != None : 
        for td in tr.select('td') :
          print(td.text.strip()+'|', end='')

      print()
import requests
import re
from bs4 import BeautifulSoup
import csv
file = open("outputs2.csv", mode="w", encoding="utf-8", newline="")
writer = csv.writer(file)

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

writer.writerow(['날짜', '종가'])

for page in range(2,5) :

  params = {
      'code' : '005930'
    ,'page' : page
  }
  res = requests.get('https://finance.naver.com/item/sise_day.naver', headers=headers, params=params)
  sams = BeautifulSoup(res.text, 'html.parser')

  for tr in sams.select('table.type2 > tr') :
    temp = []

    if tr.attrs != {} :

      if re.match('2023.08.+', tr.select('td')[0].text) != None : 

        temp.append(tr.select('td')[0].text)
        temp.append(tr.select('td')[1].text)

        # for td in tr.select('td') :
        #   temp.append(td.text.strip())

        print(temp)
        writer.writerow(temp)

file.close()
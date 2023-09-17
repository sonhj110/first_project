import requests
from bs4 import BeautifulSoup
import json
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
# yeonhap = requests.get('https://entertain.naver.com/read?oid=311&aid=0001639087', headers=headers)
# yh = BeautifulSoup(yeonhap.text, 'html.parser')


res = requests.get('https://news.like.naver.com/v1/search/contents?suppress_response_codes=true&callback=jQuery111109378512518117474_1694777838682&q=ENTERTAIN%5Bne_311_0001639087%5D%7CJOURNALIST%5B73029(period)%5D%7CENTERTAIN_MAIN%5Bne_311_0001639087%5D&isDuplication=false&cssIds=MULTI_PC%2CENTERTAIN_PC&_=1694777838683', headers=headers)

bs = BeautifulSoup(res.text, 'html.parser')

text = bs.text

# 좋아요 like
# 슬퍼요 sad
# 놀랐어요 surprise
# 응원해요 cheer
# 축하해요 congrats
# 기대해요 expect

count = 0

result = re.search('(?<=\{"reactionType\"\:\"like\"\,\"count\"\:)[0-9]+', text)
count = count + int(result.group())

result = re.search('(?<=\{"reactionType\"\:\"sad\"\,\"count\"\:)[0-9]+', text)
count = count + int(result.group())

result = re.search('(?<=\{"reactionType\"\:\"surprise\"\,\"count\"\:)[0-9]+', text)
count = count + int(result.group())

result = re.search('(?<=\{"reactionType\"\:\"cheer\"\,\"count\"\:)[0-9]+', text)
count = count + int(result.group())

result = re.search('(?<=\{"reactionType\"\:\"congrats\"\,\"count\"\:)[0-9]+', text)
count = count + int(result.group())

result = re.search('(?<=\{"reactionType\"\:\"expect\"\,\"count\"\:)[0-9]+', text)
count = count + int(result.group())

print(count)

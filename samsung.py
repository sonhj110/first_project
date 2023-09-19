import csv

new_file = open('samsung.csv', 'w', encoding='utf-8')
writer = csv.writer(new_file)

with open('news.csv', 'r', encoding='utf-8') as file :
    rdr = csv.reader(file)

    for data in rdr :
        if data[4].find('삼성전자') != -1 :
            writer.writerow(data)

new_file.close()








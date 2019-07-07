import re
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys
import warnings
from requests_html import HTMLSession

session = HTMLSession()

if not sys.warnoptions:
    warnings.simplefilter("ignore")

url_array=[]
asin_array=[]
with open('asin_list.csv', 'r') as csvfile:
    asin_reader = csv.reader(csvfile)
    for row in asin_reader:
        url_array.append(row[0])

start = 'dp/'
end = '/'
for url in url_array:
    asin_array.append(url[url.find(start)+len(start):url.rfind(end)])

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
        "x-amz-rid": input("enter your x-amz-rid: ")
    }

all_items=[]

for asin in asin_array:
    item_array=[]
    amazon_url="https://www.amazon.com/dp/"+asin
    response = session.get(amazon_url, headers=headers, verify=False)
    with open(asin + ".html", "w") as htmlfile:
        htmlfile.write(response.html.html)
    details= response.html.find("div#Price span")
    if details is None or len(details) == 0 :
        continue
    details = details[0]
    item_array.append(details.full_text)

    details_arr=[]
    details=re.sub("\n|\r", "", details)
    details_arr=re.findall(r'\>(.*?)\<', details)
    for i,row in enumerate(details_arr):
        details_arr[i]=row.replace("\t","")
    details_arr=list(filter(lambda a: a != '', details_arr))
    details_arr=[row.strip() for row in details_arr]

    for row in details_arr:
        item_array.append(row)

    all_items.append(item_array)


with open("new_file.csv","w+", encoding="utf-8") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(all_items)

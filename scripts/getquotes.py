
from __future__ import print_function
import requests,argparse,os
from bs4 import BeautifulSoup
import unicodecsv as csv
import pprint

headers = {
'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}


##parse initial url and parse pagination and return list of pagination urls
def ParseUrl(url):
	req = requests.get(url,headers=headers)
	soup = BeautifulSoup(req.content,'lxml')
	last_page = soup.find(text='Next')
	if last_page is not None:
		page = last_page.find_previous('li').find_previous('li')
		page_url = ('https://www.brainyquote.com'+
		page.a['href'].split('&')[0]+'&pg=')
		return [page_url+str(x) for x in range(1,int(page.text)+1)]
	else:
		return None

##requests each page, parse and return list of dictionary
def Parse(url,data=[]):
	req = requests.get(url,headers=headers)
	soup = BeautifulSoup(req.content,'lxml')
	quotes = soup.find_all('div',attrs={'class':'qll-bg'})
	if quotes is not None:
		for x in quotes:
			Quote = x.find(title='view quote')
			Author = x.find(title='view author')
			Tags = x.find(class_='kw-box')
			parse_data = {
			'Quote':Quote.text.strip() if Quote else'',
			'Author':Author.text.strip() if Author else'',
			'Tags':Tags.text.strip().replace('\n',', ') if Tags else'',
			'QuoteUrl':'https://www.brainyquote.com'+Quote['href'] if Quote else'',
			'AuthorUrl':'https://www.brainyquote.com'+Author['href'] if Author else''
			}
			data.append(parse_data)
	return data

			

if __name__ == '__main__':
	##command line arguments
	argparser = argparse.ArgumentParser()
	argparser.add_argument('keyword',help='Search Keyword')
	args = argparser.parse_args()
	keyword = args.keyword
	url = ('https://www.brainyquote.com/search_results?q={}'
		.format(keyword.replace(' ','+')))
	##parse urls
	data = ParseUrl(url)
	##create csv file for writing the data
	filename = 'quotes.csv'
	file_exists = os.path.isfile(filename)
	with open(filename, 'ab') as f:
		fieldnames = ['Quote','Author','Tags','QuoteUrl','AuthorUrl']
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		if not file_exists:
			writer.writeheader()

		if data:##multipages
			for url in data:
				pp = Parse(url)
				if pp is not None:
					writer.writerows(pp)
					pprint.pprint(pp)
				
		else:##single pages
			pp = Parse(url)
			if pp is not None:
				writer.writerows(pp)
				pprint.pprint(pp)



""" proceding to re-work the initial bs4 HTML exploration -> 
	successfully walking through the full site and collecting desired data to JSON """

import json
import requests
from bs4 import BeautifulSoup

header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}

resp = requests.get('https://www.precisionnutrition.com/encyclopedia', headers=header)
soup = BeautifulSoup(resp.content, 'lxml')

toc_strings = [item.find('h3').get_text() for item in soup.find_all('div', class_='food-category')]

# Collecting URLS:
for string in toc_strings:
	url_ul = soup.find(string=string).find_parent(class_="food-category").find('ul')
	url_list = [url.get('href') for url in url_ul.find_all('a')]

	# Scraping to JSON:
	category_object = []
	for url in url_list:

		elementDict = {}
		element_url = url
		resp = requests.get(element_url, headers=header)
		soup = BeautifulSoup(resp.content, 'lxml')

		elementDict.update({"name": url.split('food/')[1]})

		nav_strings = [item.get('id') for item in soup.find('div', class_="food-item__content").find_all('section')]
		nav_strings = [e for e in nav_strings if e not in ['recipe', 'updates', 'related-foods']]

		for nav_id in nav_strings:
			section = soup.find('section', id=nav_id)
			ele_list = [p.get_text() for p in section.find_all(['p', 'li'])]
			elementDict.update({nav_id: [e for e in ele_list]})
			ele_list = []

		category_object.append(elementDict)

	resp = requests.get('https://www.precisionnutrition.com/encyclopedia', headers=header)
	soup = BeautifulSoup(resp.content, 'lxml') # reset request

	string = string.lower().replace(' ', '_')	

	with open('encyclopedia/{}.json'.format(string), 'w') as write_file:
		json.dump(category_object, write_file, indent=4)





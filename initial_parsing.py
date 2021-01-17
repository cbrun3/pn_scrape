""" the process of initially exploring the site's HTML with bs4
	and outlining the JSON format desired in result """

import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}

""" # Making the initial request:
resp = requests.get('https://www.precisionnutrition.com/encyclopedia', headers=header)
soup = BeautifulSoup(resp.content, 'lxml')
print(soup.prettify()) 
"""

""" # Collecting urls:
macroUL = soup.find(string='Micronutrients').find_parent(class_="food-category").find('ul')

macroURLS = []
for url in macroUL.find_all('a'):
	macroURLS.append(url.get('href'))

s = pd.Series(macroURLS)
s.to_pickle('macrourls.pickle')
"""


## Scraping to JSON:
s = pd.read_pickle('macrourls.pickle')
print(s)

micronutrients = []
for url in s:
	microurl = url
	resp = requests.get(microurl, headers=header)
	soup = BeautifulSoup(resp.content, 'lxml')

	name = url.split('food/')[1]
	print('name', name)

	section = soup.find('div', class_='food-item__summary')
	at_a_glance = []
	for p in section.find_all(['p', 'li']):
		at_a_glance.append(p.get_text())
	print('\nat_a_glance', at_a_glance)

	section = soup.find('section', id='overview')
	overview = []
	for p in section.find_all(['p', 'li']):
		overview.append(p.get_text())
	print('\noverview', overview)

	section = soup.find('section', id='importance')
	importance = []
	for p in section.find_all(['p', 'li']):
		importance.append(p.get_text())
	print('\nimportance', importance)

	section = soup.find('section', id='food-sources')
	sources = []
	for p in section.find_all(['p', 'li']):
		sources.append(p.get_text())
	print('\nsources', sources)

	section = soup.find('section', id='deficiencies')
	deficiencies = []
	for p in section.find_all(['p', 'li']):
		deficiencies.append(p.get_text())
	print('\ndeficiencies', deficiencies)

	section = soup.find('section', id='excess-toxicity')
	excess_toxicity = []
	for p in section.find_all(['p', 'li']):
		excess_toxicity.append(p.get_text())
	print('\nexcess_toxicity', excess_toxicity)

	print('\n#############################\n')

	micronutrients.append({
		"name": name,
		"at_a_glance": [e for e in at_a_glance],
		"overview": [e for e in overview],
		"importance": [e for e in importance],
		"sources": [e for e in sources],
		"deficiencies": [e for e in deficiencies],
		"excess_toxicity": [e for e in excess_toxicity]
		})


with open('micronutrients.json', 'w') as write_file:
	json.dump(micronutrients, write_file, indent=4)




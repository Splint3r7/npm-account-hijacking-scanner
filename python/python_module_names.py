import requests
from bs4 import BeautifulSoup
import concurrent.futures

BASE_URI = "https://pypi.org"

def ExtractClassirfiers():

	classifier = []

	req = requests.get("https://pypi.org/classifiers/")
	soup = BeautifulSoup(req.text, 'html.parser')
	atags = soup.find_all("a")
	for x in atags:
			b = x['href']
			if "/search/?c=" in b:
				c = BASE_URI+b
				classifier.append(c)

	return classifier

def ExtractLastPage(URL: str):

	pages = []
	try: 
		req = requests.get(URL)
		soup = BeautifulSoup(req.text, 'html.parser')
		atags = soup.find_all("a", {"class": "button button-group__button"})
		for tag in atags:
			x = tag['href']
			x = x.split("=")
			p = int(x[2])
			pages.append(p)
		return max(pages)
	except:
		page = int(1)
		return page

def ExtractModuleNmaes(URL: str):

	req = requests.get(URL)
	soup = BeautifulSoup(req.text, 'html.parser')
	spans = soup.find_all("span", {"class": "package-snippet__name"})
	for spant in spans:
		print(spant.get_text())

if __name__ == "__main__":

	listClassifier = ExtractClassirfiers()

	for classifierUrls in listClassifier:
		pageNum = ExtractLastPage(classifierUrls)
		for pagenumCounter in range(1, int(pageNum)):
			URL = classifierUrls+"&page="+str(pagenumCounter)
			name = ExtractModuleNmaes(URL)
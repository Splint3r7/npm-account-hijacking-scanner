import requests
from bs4 import BeautifulSoup
import concurrent.futures

output = open("ruby_gems.txt", "a")

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

def LastPage(letter: str):

	lastPageNum = ""
	req = requests.get("https://rubygems.org/gems?letter={}".format(letter))
	soup = BeautifulSoup(req.text, 'html.parser')
	atags = soup.find_all("a")
	for x in atags:
		if "Last »" in x:
			b = x['href']
			sp  = b.split("=")[2]
			lastPageNum = sp
	return lastPageNum

def ExtractConent():

	url = "https://rubygems.org/gems?letter=A&page=1"
	req = requests.get(url)
	soup = BeautifulSoup(req.text, 'html.parser')
	atags = soup.find_all("h2", {"class": "gems__gem__name"})
	for tag in atags:
		print(tag.contents[0].strip())

def ExtractNames(letter: str):

	letter = letter.strip()
	LastPageN = LastPage(letter)
	for number in range(1, int(LastPageN)):
		URL = "https://rubygems.org/gems?letter={}&page={}".format(letter, number)
		req = requests.get(URL)
		soup = BeautifulSoup(req.text, 'html.parser')
		atags = soup.find_all("h2", {"class": "gems__gem__name"})
		for tag in atags:
			results = tag.contents[0].strip()
			print(results)
			output.write(results+"\n")

if __name__ == "__main__":

	with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
		executor.map(ExtractNames, letters)

  output.close()
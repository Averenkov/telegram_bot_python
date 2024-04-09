import requests
import wget
from bs4 import BeautifulSoup

def get_music(s):
	url = 'https://ru.hitmotop.com/search?q=' + s
	headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
	g = BeautifulSoup(requests.get(url, headers=headers).text, 'lxml').find('ul', {'class' : 'tracks__list'}).find('li')
	return wget.download(g.find('a', {'class' : 'track__download-btn'})['href'])
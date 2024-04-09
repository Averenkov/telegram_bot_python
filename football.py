import requests
from datetime import datetime

def bold(s):
	return '*' + s + '*'

def get_football_mathes():
	dt = datetime.now().date()
	headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

	r = requests.get("https://www.championat.com/stat/football/"+str(dt)+".json", headers=headers)

	js = r.json()['matches']['football']['tournaments']

	cnt = 0

	ans = ''

	for i in js:
		name_champ = js[i]['name']
		ans += bold(name_champ) + '\n'
		matches = js[i]['matches']
		ans += '\n'
		ans += '----------------------------------\n'
		for j in matches:
			ans += j['time_str'] + ' ' + j['status']['name'] + '\n'
			ans += j['teams'][0]['name'] + ' - ' + j['teams'][1]['name'] + '\n'
			if j['status']['label'] != 'dns':
				ans += 'Счет: ' + str(j['score']['direct']['main']) + '\n'
			try:
				ans += 'П1: ' + bold(j['coeffs']['RU']['f']) + ' X: ' + bold(j['coeffs']['RU']['d']) + ' П2: ' + bold(j['coeffs']['RU']['s']) + '\n'
			except:
				pass
			ans += '----------------------------------\n'
		ans += '\n' * 2
		cnt += 1
		if cnt == 6:
			break
	return ans

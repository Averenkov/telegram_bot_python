import requests

def get_translate(s):

	url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

	payload = {
		"q": s,
		"target": "en",
		"source": "ru"
	}
	headers = {
		"content-type": "application/x-www-form-urlencoded",
		"Accept-Encoding": "application/gzip",
		"X-RapidAPI-Key": "a1d79e6ce6mshe4df3b40931c049p1cd69ajsnd3db0afc8962",
		"X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
	}

	response = requests.post(url, data=payload, headers=headers)
	return response.json()['data']['translations'][0]['translatedText']

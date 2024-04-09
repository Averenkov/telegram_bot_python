import requests
from bs4 import BeautifulSoup
import datetime
import json
import pylab
import matplotlib.dates


def get_today_date():
	date = str(datetime.datetime.now().date()).split('-')
	date.reverse()
	return '.'.join(date)
def get_pretty_date(date):
	date = str(date).split('-')
	date.reverse()
	return '.'.join(date)
def prety_date_to_date(date):
	date = date.split('.')
	return datetime.date(int(date[2]), int(date[1]), int(date[0]))

class requestsCurrency:
	def __new__(self):
		if not hasattr(self, 'instance'):
			self.instance = super(requestsCurrency, self).__new__(self)
		return self.instance
	def __init__(self):
		self.url_cb = 'https://www.cbr.ru/currency_base/daily/'
		self.url_cb_period = 'https://www.cbr.ru/currency_base/dynamics/'
		self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
		self.info = dict()
		self.update_info(get_today_date())
		self.value_name = dict()
	def get_info_by_date(self, date):
		data = {'unidbquery.posted' : 'True', 'unidbquery.to' : date}
		headers = {'user-agent' : self.user_agent}
		table = BeautifulSoup(requests.get(self.url_cb, headers=headers, data=data).text, 'lxml').find('table', {'class' : 'data'})
		currencies = table.find_all('tr')[1::]
		ans = dict()
		for i in currencies:
			ans[i.find_all('td')[3].text] = i.find_all('td')
		return ans
	def update_info(self, date):
		if date not in self.info:
			self.info[date] = self.get_info_by_date(date)
	def get_value(self, date, name):
		self.update_info(date)
		return float(self.info[date][name][-1].text.strip().replace(',', '.')) / int(self.info[date][name][-3].text.strip())
	def get_names(self):
		names = []
		today_date = get_today_date()
		self.update_info(today_date)
		return self.info[today_date].keys()
	def _get_value_by_name(self):
		if len(self.value_name) != 0:
			return
		form = BeautifulSoup(requests.get(self.url_cb_period).text, 'lxml').find('select', {'name' : 'UniDbQuery.VAL_NM_RQ'})
		forms = form.find_all('option')
		for i in forms:
			self.value_name[i.text.strip()] = i['value']
	def get_values_period(self, name, date_from, date_to):
		self._get_value_by_name()
		data = {'UniDbQuery.Posted' : 'True',
				'UniDbQuery.so' : '1',
				'UniDbQuery.mode' : '1',
				'UniDbQuery.VAL_NM_RQ' : self.value_name[name],
				'UniDbQuery.From' : date_from,
				'UniDbQuery.To' : date_to
		}
		headers = {'user-agent' : self.user_agent}
		r = requests.get(self.url_cb_period, headers=headers, params=data)
		table = BeautifulSoup(r.text, 'lxml').find('table', {'class' : 'data'})
		currencies = table.find_all('tr')[2::]
		ans = dict()
		for i in currencies:
			ans[i.find_all('td')[0].text] = i.find_all('td')
		return ans
class Currency:
	def __init__(self, name):
		self.rCurrency = requestsCurrency()
		self.name = self.filter_name(name[0].upper() + name.lower()[1::])
		if self.name == None:
			return
		self.today_value = self.update_value(get_today_date())
	def check_name(self, name1, name2):
		uk = 0
		cnt = 0
		for i in name2:
			while uk < len(name1) and name1[uk] != i:
				uk += 1
			if uk == len(name1):
				break
			cnt += 1
			uk += 1
		return ((cnt > 0.7 * len(name1)) or (cnt > 0.7 * len(name2)))
	def filter_name(self, name):
		names = self.rCurrency.get_names()
		for i in names:
			if self.check_name(i, name):
				return i
		return None
	def update_value(self, date=get_today_date()):
		return self.rCurrency.get_value(date, self.name)

	def get_values_period(self, date_from, date_to):
		ans = self.rCurrency.get_values_period(self.name, get_pretty_date(date_from), get_pretty_date(date_to))
		true_ans = dict()
		for i in ans:
			true_ans[i] = float(ans[i][-1].text.strip().replace(',', '.')) / int(ans[i][-2].text.strip())
		return true_ans
	def get_name(self):
		return self.name
	def check_input_name(self, name):
		name = name[0].upper() + name.lower()[1::]
		return self.check_name(self.name, name)

def get_graphs(c1, c2, date_from, date_to):
	date_from = prety_date_to_date(date_from)
	date_to = prety_date_to_date(date_to)

	if c1 != 'рубль':
		ans1 = c1.get_values_period(date_from, date_to)
	else:
		ans1 = '#'
	if c2 != 'рубль':
		ans2 = c2.get_values_period(date_from, date_to)
	else:
		ans2 = '#'

	xdata = []
	ydata = []

	for i in ans1:
		xdata += [prety_date_to_date(i)]
		y = 1
		x = 1
		if ans1 != '#':
			y = ans1[i]

		if ans2 != '#':
			x = ans2[i]
		ydata += [y / x]
	xdata_float = matplotlib.dates.date2num(xdata)

	axes = pylab.subplot(1, 1, 1)

	axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d-%m-%y'))

	pylab.plot_date (xdata_float, ydata, fmt="b-")

	pylab.grid()
	pylab.savefig('graph.png', dpi = 100)

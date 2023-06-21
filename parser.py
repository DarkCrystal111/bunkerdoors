import requests
import lxml
from bs4 import BeautifulSoup

class Parser:
	def __init__(self):
		self.url = "https://bunkerdoors.ru"
		self.data = []
		self.buffer = []

	def get_all_doors(self):
		resp = requests.get(self.url+"/prod")
		if not resp.ok:
			debug(resp)
			return False
		soup = BeautifulSoup(resp.content, "lxml")
		t1 = soup.find(class_="sections-01__inner")
		for x in t1.findChild().findAll('li'):
			inside_url = x.findNext().attrs["href"]
			name = x.text.strip()
			self.data.append({"url": self.url+inside_url, "name": name})
		return True

	def between(self):
		for x in self.data:
			url = x['url']
			resp = requests.get(url+".json?sort=position&direction=asc&page=1")
			if not resp.ok:
				debug(resp)
			info = resp.json()
			pages = info["meta"]["total_pages"]
			self.get_info(info["products"])
			if str(pages) == "1":
				continue
			for n in range(2, pages+1):
				resp = requests.get(url+".json?sort=position&direction=asc&page="+str(n))
				if not resp.ok:
					debug(resp)
				info = resp.json()["products"]
				self.get_info(info)


	def get_info(self, info):
		for x in info:
			uid = x['id']
			name = x['name']
			path = "https://bunkerdoors.ru"+x['path']
			image = [n['original_path'] for n in x['images']]
			current_price = x['price']
			if x['has_old_price'] == 'false':
				past_price = False
			else:
				past_price = x['old_price']
			obj = {"id": uid, "name": name, "path": path, "images": image,
			"current_price": current_price, "past_price": past_price}
			self.buffer.append(obj)


	@staticmethod
	def debug(resp):
		print(resp.reason)
		exit(1)

	def menu(self):
		self.get_all_doors()
		self.between()
		with open("js.json", "w+") as f:
			print(self.buffer,file=f)
		print(self.buffer)
a = Parser()
a.menu()
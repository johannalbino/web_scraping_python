import os
try:
	import pandas as pd
	import requests
	from selenium import webdriver
	from bs4 import BeautifulSoup
	from selenium.webdriver.support import expected_conditions as EC
	from selenium.webdriver.remote.webelement import WebElement
	from selenium.webdriver.support.wait import WebDriverWait
	from selenium.webdriver.common.by import By
	import time
	from PIL import Image, ImageOps, ImageEnhance

except:
	os.system('pip install pandas')
	os.system('pip install selenium')
	os.system('pip install pytesseract')
	os.system('pip install beautifulsoup4')
	os.system('pip install Pillow')


class WebScraper(object):

	def __init__(self, url):
		self.__req = url
		self.__df = pd.DataFrame()
		self.__driver = webdriver.Chrome(executable_path="chromedriver.exe")

	def search_company(self, pesquisar):
		while True:
			req_url = self.__req + pesquisar
			self.__driver.get(req_url)
			captcha = self.__driver.find_element_by_xpath('//*[@id="formBuscaAvancada"]/table/tbody/tr[1]/td/div/div[2]/label/input') # find input
			captcha.clear()
			print('Digite o código da imagem no browser.')

			try:
				table_info = EC.presence_of_element_located((By.ID, 'ctl00_cphContent_gdvResultadoBusca_gdvContent'))
				WebDriverWait(self.__driver, 10).until(table_info)
				html = self.__driver.page_source
				soup = BeautifulSoup(html, 'lxml')
				table = soup.find('table', {'id': 'ctl00_cphContent_gdvResultadoBusca_gdvContent'})
				df = pd.read_html(str(table))[0]
				self.__df = self.__df.append(df)
				self.__driver.close()
				return self.__df
			except Exception as e:
				print('\nO código da imagem está incorreto, digite novamente.')


url = 'https://www.jucesponline.sp.gov.br/ResultadoBusca.aspx?ppe='
websc = WebScraper(url)
company = input('Digite o nome da empresa, razao social ou NIRE: ')
data = websc.search_company(company)

_data = data.to_dict('split')
new_data = []
keys = _data['columns']
keys.pop()
for dat in _data['data']:
	new_data.append(dict(zip(keys, dat)))

print(new_data[:10])


import os

try:
	import pandas as pd
	from selenium.common.exceptions import TimeoutException
	import requests
	import re
	from selenium import webdriver
	from selenium.webdriver.support import expected_conditions as EC
	from selenium.webdriver.common.by import By
	from bs4 import BeautifulSoup
	from selenium.webdriver.remote.webelement import WebElement
	from selenium.webdriver.support.wait import WebDriverWait
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
		self.__info = {}

	def search_company(self, nire):
		req_url = self.__req.format('', nire)
		validate = True
		while validate:
			self.__driver.get(req_url)
			captcha = self.__driver.find_element_by_xpath('//*[@id="formBuscaAvancada"]/table/tbody/tr[1]/td/div/div[2]/label/input') # find input
			captcha.clear()
			print('Digite o código da imagem no browser.')
			try:
				table_info = EC.presence_of_element_located((By.ID, 'ctl00_cphContent_frmPreVisualiza_lblEmpresa'))
				WebDriverWait(self.__driver, 10).until(table_info)
				self.__info['nome'] = self.__driver.find_element_by_css_selector('#ctl00_cphContent_frmPreVisualiza_lblEmpresa').text
				self.__info['Tipo de Empresa'] = self.__driver.find_element_by_css_selector('#ctl00_cphContent_frmPreVisualiza_lblDetalhes').text
				self.__info['Inicio de Atividade'] = self.__driver.find_element_by_css_selector('#ctl00_cphContent_frmPreVisualiza_lblAtividade').text
				self.__info['cnpj'] = self.__driver.find_element_by_css_selector('#ctl00_cphContent_frmPreVisualiza_lblCnpj').text
				self.__info['nire'] = self.__driver.find_element_by_css_selector('#ctl00_cphContent_frmPreVisualiza_lblNire').text
				self.__info['data da constituicao'] = self.__driver.find_element_by_css_selector('#ctl00_cphContent_frmPreVisualiza_lblConstituicao').text
				self.__info['inscricao estadual'] = self.__driver.find_element_by_css_selector('#ctl00_cphContent_frmPreVisualiza_lblInscricao').text
				self.__info['objetivo'] = self.__driver.find_element_by_css_selector('#ctl00_cphContent_frmPreVisualiza_lblObjeto').text
				self.__info['capital'] = self.__driver.find_element_by_css_selector('#ctl00_cphContent_frmPreVisualiza_lblCapital').text
				self.__info['logradouro'] = self.__driver.find_element_by_css_selector('#ctl00_cphContent_frmPreVisualiza_lblLogradouro').text
				self.__info['numero'] = self.__driver.find_element_by_css_selector('#ctl00_cphContent_frmPreVisualiza_lblNumero').text
				self.__info['bairro'] = self.__driver.find_element_by_css_selector('#ctl00_cphContent_frmPreVisualiza_lblBairro').text
				self.__info['complemento'] = self.__driver.find_element_by_css_selector('#ctl00_cphContent_frmPreVisualiza_lblComplemento').text
				self.__info['municipio'] = self.__driver.find_element_by_css_selector('#ctl00_cphContent_frmPreVisualiza_lblMunicipio').text
				self.__info['cep'] = self.__driver.find_element_by_css_selector('#ctl00_cphContent_frmPreVisualiza_lblCep').text
				self.__info['uf'] = self.__driver.find_element_by_css_selector('#ctl00_cphContent_frmPreVisualiza_lblUf').text
				validate = False
				self.__driver.close()
				return self.__info
			except TimeoutException:
				validate = True
				print('\nO código da imagem está incorreto, digite novamente.')


url = 'https://www.jucesponline.sp.gov.br/Pre_Visualiza.aspx?idproduto={0}&nire={1}'
websc = WebScraper(url)
company = input('Digite o NIRE: ')
company = re.findall(r'\d+', company)
data = websc.search_company(company[0])
print(data)


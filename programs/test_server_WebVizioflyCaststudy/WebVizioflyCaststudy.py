import requests
from bs4 import BeautifulSoup
def viziofly_casestudy():
    source=requests.get('https://www.viziofly.com/#installationart')
    content=BeautifulSoup(source.text,'html.parser')
    tag=content.find_all('div',class_='item-details')
    for i in tag:
        a=i.find('h1',class_='portfolio-grid-title white')
        print(a.text)
Start=input('Do you want to continute read through recent casestudy from viziofly? \nType Y/N and Enter')
if Start=='Y':
    viziofly_casestudy()

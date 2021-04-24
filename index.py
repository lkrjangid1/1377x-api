import requests
from bs4 import BeautifulSoup
from re import search
from flask import Flask ,jsonify
import json
import os
import concurrent.futures

app = Flask(__name__)
app.url_map.strict_slashes = False

product_name = []
product_url = []
product_icon = []
product_plateform = []
product_size = []

def filecrSearch(title):
    for i in range(1,40):
        url = f'https://filecr.com/?page={i}&s={title}'

        header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

        r = requests.get(url, headers=header)
        soup = BeautifulSoup(r.content,features='lxml')
        articals = soup.find_all('div', class_ ='product')

        for item in articals:
            product_name.append(item.find('a', class_ = 'product-title'))
            product_url.append(item.find('a', class_ = 'product-icon')['href'])
            product_size.append(item.find('div', class_='side-border product-size').text)
            product_plateform.append(item.find('span', class_='text').text)
            product_icon.append(item.find('img')['src'])
            

@app.route('/')
def home_page():
    return "Welcome to 1337x unofficial API"

@app.route('/<query>')
def home(query):
    filecrSearch(query)

    return jsonify([{'Name':product_name[index],
    'size':product_size[index],
    'url':product_url[index],
    'icon': product_icon[index],
    'plateform':product_plateform[index],
    } 
    for index in range(len(product_name))])



if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)

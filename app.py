  
import requests
from bs4 import BeautifulSoup
from flask import Flask ,jsonify
import json
import os
import re
import concurrent.futures


app = Flask(__name__)
app.url_map.strict_slashes = False


def torrent(search):
    url = "https://1337x.to/search/"+search+"/1/"

    res = requests.get(url,headers={
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'})
                
    soup = BeautifulSoup(res.content,'lxml')
    
    link_list = []

    for a in soup.find_all('a', href=True, text=True):
        link_text = str(a['href'])
        if link_text.startswith("/torrent"):
            link_text = "https://1337x.to"+link_text
            link_list.append(link_text)
    
    file_name = []
    magnet_url_list = []
    total_downloads_list = []
    last_checked_list = []
    total_downloads_list = []
    last_checked_list = []
    date_uploaded_list = []
    file_size = []
    date_uploaded_list = []
    seeder_list = []
    leecher_list =[]
    language_list =[]
    category_list = []
    type_list = []
    
    

    def get_all_data_torrent(url_list):
        magnet_req = requests.get(url_list,headers={
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'})
        new_soup = BeautifulSoup(magnet_req.content,'lxml')
        
        everything_data_list = []

        div = new_soup.find('div',class_='box-info-heading').text
        file_name.append(div)
        for span in new_soup.find_all('span'):
            if span.text != "":
                everything_data_list.append(span.text)

        category_list.append(everything_data_list[1])
        type_list.append(everything_data_list[2])
        total_downloads_list.append(everything_data_list[6])
        last_checked_list.append(everything_data_list[7])
        date_uploaded_list.append(everything_data_list[8])
        file_size.append(everything_data_list[4])
        seeder_list.append(everything_data_list[9])
        leecher_list.append(everything_data_list[10])
        language_list.append(everything_data_list[3])
        
        magnet_url = re.findall(r"\"magnet:.*?\"",str(magnet_req.content))[0].strip(" \" ")

        magnet_url_list.append(magnet_url)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_all_data_torrent,link_list)
    
    return file_name,file_size,link_list,date_uploaded_list,seeder_list,leecher_list,magnet_url_list,total_downloads_list,last_checked_list,language_list,type_list,category_list
@app.route('/')
def home_page():
    return "Welcome to 1337x unofficial API"

@app.route('/<query>')
def home(query):

    file_name,file_size,link_list,date_uploaded_list,seeder_list,leecher_list,magnet_url_list,total_downloads_list,last_checked_list,language_list,category_list,type_list = torrent(query)

    return jsonify([{'Name':file_name[index],
    'size':file_size[index],'url':link_list[index],
    'uploadDate': date_uploaded_list[index],
    'seeders':seeder_list[index],
    'leechers': leecher_list[index],
    'magnet': magnet_url_list[index],
    'downloads':total_downloads_list[index],
    'lastChecked': last_checked_list[index],
    'language': language_list[index],
    'category': category_list[index],
    'type': type_list[index]} 
    for index in range(len(file_name))])



if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)

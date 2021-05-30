# Kivano
# Написать парсер сайта kivano. (Название, стоимость, описание, наличие, ссылка на сам товар)
# pip intall BeautifulSoup4
from bs4 import BeautifulSoup
# pip intall requests
import requests
import csv


CSV = 'kivano_parser.csv'
HOST = 'https://www.kivano.kg'
URL = 'https://www.kivano.kg/noutbuki'

HEADERS = {
    'Accep' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;*/*;q=0.9', 
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params, verify=False)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_ = 'pull-right rel')
    new_list = []

    for item in items:
        new_list.append({
            # это вывод название товара
            'title' : item.find('div', class_ = 'listbox_title oh').get_text(strip=True),
            # стоимость выыода товара
            'price' : item.find('div', class_ = 'listbox_price text-center').get_text(strip=True),
            # описание товара
            'description' : item.find('div', class_ = 'product_text pull-left').get_text(strip=True),
            # наличе товара 
            'availability' : item.find('div', class_ = 'listbox_motive text-center').get_text(strip=True),
            # ссылка на товар
            'link' : HOST + item.find('a').get('href'),
            # find('div', class_='listbox_img pull-left').



        })
    return new_list



def news_save(items, path):
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=';')
        # Название, стоимость, описание, наличие, ссылка на сам товар
        writer.writerow(['Названия','Описание товара', 'в наличие товара', 'Ссылка на товар'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['description'], item['availability'], item ['link']])

def parser():
    PAGENATION = input("Введите количество страниц: ")
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        news_list = []
        for page in range(1, PAGENATION):
            print(f'Страница №{page} готова')
            html = get_html(URL, params={'page' : page})
            news_list.extend(get_content(html.text))
        news_save(news_list, CSV)
        print('Парсинг готов')
    else:
        print('Error')

parser()


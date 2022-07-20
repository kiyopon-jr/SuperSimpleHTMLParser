import requests
from bs4 import BeautifulSoup
import csv

CSV = 'ot.csv'
HOST = "https://zagruzka.online/"
URL = "https://zagruzka.online/katalog/verhny-odyag-xl/"
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 '
                  'Safari/537.36 '
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='ty-column3')
    outerwear = []
    for item in items:
        outerwear.append(
            {
                'title': item.find('div', class_='ty-grid-list__item-name').find('a').get_text(strip=True),
                'link': item.find('div', class_='ty-grid-list__item-name').find('a').get('href'),
            }
        )
    return outerwear


def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['link']])


def parser():
    PAGE = int(input('Укажите кол-во страниц для парсинга:'))
    html = get_html(URL)
    if html.status_code == 200:
        outerwear = []
        for page in range(1, PAGE + 1):
            print(f'Парсим страницу: {page}')
            html = get_html(URL, params={'page': page})
            outerwear.extend(get_content(html.text))
        save_doc(outerwear, CSV)
        print(outerwear)
    else:
        print('Error')


parser()

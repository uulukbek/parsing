import requests
from bs4 import BeautifulSoup as b 
import csv


def save_(data):
    with open('notebooks.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter='/')
        writer.writerow((data['title'],
                        data['price'],
                        data['photo']))

def get_html(url):
    response = requests.get(url)
    return response.text


def get_total_pages(html):
    soup = b(html, 'lxml')
    pages_ul = soup.find('div', class_='bx-pagination-container row').find('ul')
    last_page = pages_ul.find_all('li')[-2]
    total_pages = last_page.find('a').get('href').split('1=')[-1]
    return int(total_pages)


def get_page_data(html):
    soup = b(html,'lxml')
    product_list = soup.find('div', class_='items productList')
    products = product_list.find_all('div', class_='item product sku')

    for product in products:
        
        try:
            photo = product.find('div', class_='productColImage').find('a').find('img').get('src')
        except:
            photo = ''

        
        try:
            title = product.find('div', class_='productColText').find('a').text
        except:
            title = ''

        
        try:
            price = product.find('div', class_='productColText').find('a', class_='price').text
        except:
            price = ''

        
        data = {'price':price, 'title':title, 'photo':photo}
        save_(data)

def main():
    notebooks_url = 'https://ultra.kg/catalog/noutbuki-planshety-i-kompyutery/noutbuki/?gclid=EAIaIQobChMI3tCV0eGe_AIVTUiRBR1vOgoUEAAYASAAEgIkMvD_BwE_1='
    pages = '_1='
    total_pages = get_total_pages(get_html(notebooks_url))


    for page in range(1, total_pages+1):
        pu=notebooks_url + pages + str(page)
        html = get_html(pu)
        get_page_data(html)

main()
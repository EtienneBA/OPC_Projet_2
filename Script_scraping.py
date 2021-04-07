import requests
from bs4 import BeautifulSoup
from math import *

links = []

url_category = 'http://books.toscrape.com/catalogue/category/books/cultural_49/index.html'
response = requests.get(url_category)
if response.ok:
    soup = BeautifulSoup(response.text,'lxml')
    nombre_livres = soup.find('form', {'class' : 'form-horizontal'}).find('strong')
    nombre_pages = ceil(int(nombre_livres.text) / int(20))
    print('Nombre de pages: ', nombre_pages)

if nombre_pages > 1:
    for i in range(1,nombre_pages+1):
        url_page = url_category.replace("index.html","") + 'page-' + str(i) + '.html'
        print(url_page)
        response = requests.get(url_page)
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')

            livre = soup.findAll('article')

            for article in livre:
                a = article.find('a')
                link = a['href']
                links.append('http://books.toscrape.com/catalogue/' + link[9:])

    with open ('urls.txt', 'w') as file:
        for link in links:
            file.write(link + '\n')

    with open ('urls.txt', 'r') as inf:
        with open ('bouquin.csv', 'w', encoding="utf8") as outf:
            outf.write('upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating\n')
            for row in inf:
                url = row.strip()
                response = requests.get(url)
                if response.ok:
                    soup = BeautifulSoup(response.text, 'lxml')

                    universal_product_code = soup.find('td').text
                    title = soup.find('h1').text
                    price_including_tax = soup.find('th', text='Price (incl. tax)').find_next('td').text[1:]
                    price_excluding_tax = soup.find('th', text='Price (excl. tax)').find_next('td').text[1:]
                    number_available = soup.find('th', text='Availability').find_next('td').text
                    product_description = soup.find('h2').find_next().text
                    category = soup.find('a').find_next('a').find_next('a').find_next('a').text
                    review_rating = soup.find('p', class_='star-rating')['class'][1]
                    image_url = soup.find('img')['src']

                    outf.write(universal_product_code + ',' + title + ',' + price_including_tax + ',' + price_excluding_tax + ',' + number_available + ',' + product_description.replace(',', '') + ',' + category + ',' + review_rating + '\n')
                    print(universal_product_code)
else:

    print(url_category)
    response = requests.get(url_category)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')

        livre = soup.findAll('article')

        for article in livre:
            a = article.find('a')
            link = a['href']
            links.append('http://books.toscrape.com/catalogue/' + link[9:])

with open('urls.txt', 'w') as file:
    for link in links:
        file.write(link + '\n')

with open('urls.txt', 'r') as inf:
    with open('bouquin.csv', 'w', encoding="utf8") as outf:
        outf.write(
            'upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating\n')
        for row in inf:
            url = row.strip()
            response = requests.get(url)
            if response.ok:
                soup = BeautifulSoup(response.text, 'lxml')

                universal_product_code = soup.find('td').text
                title = soup.find('h1').text
                price_including_tax = soup.find('th', text='Price (incl. tax)').find_next('td').text[1:]
                price_excluding_tax = soup.find('th', text='Price (excl. tax)').find_next('td').text[1:]
                number_available = soup.find('th', text='Availability').find_next('td').text
                product_description = soup.find('h2').find_next().text
                category = soup.find('a').find_next('a').find_next('a').find_next('a').text
                review_rating = soup.find('p', class_='star-rating')['class'][1]
                image_url = soup.find('img')['src']

                outf.write(universal_product_code + ',' + title + ',' + price_including_tax + ',' + price_excluding_tax + ',' + number_available + ',' + product_description.replace(',', '') + ',' + category + ',' + review_rating + '\n')
                print(universal_product_code)
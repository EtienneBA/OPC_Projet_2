import requests
from bs4 import BeautifulSoup
from math import *

url = 'http://books.toscrape.com/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
categories = {}

# Je crée un fichier 'url_category_listing.txt' regroupant les urls de chaque catégorie
with open('url_category_listing.txt', 'w') as file:

        find_all_a = soup.find('div', class_= 'side_categories').find('ul').find_next('ul').find_all(href=True)
        for el in find_all_a:
            name = el.text.strip()
            print(name)
            categories[name] = 'http://books.toscrape.com/' + el['href']
            print('http://books.toscrape.com/' + el['href'])
            file.write('http://books.toscrape.com/' + el['href'] + '\n')

for key in categories:
    print(key,': ', categories[key])



links = []
# J'ouvre mon fichier 'url_category_listing.txt' fraichement créé
with open('url_category_listing.txt', 'r') as file:

    # J'itère au sein de ce fichier 'url_category_listing.txt' pour aller chercher les adresses des catégories
    for row in file:
        url_category = row.strip()
        response = requests.get(url_category)
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')
            nombre_livres = soup.find('form', {'class': 'form-horizontal'}).find('strong')
            nombre_pages = ceil(int(nombre_livres.text) / int(20))
            print('Nombre de pages: ', nombre_pages)

            # Si j'ai plusieurs page au sein d'une catégorie, je fais ça pour naviguer au sein des pages et obtenir tous l'URL de chaque livre:
            if nombre_pages > 1:
                for i in range(1, nombre_pages + 1):
                    url_page = url_category.replace("index.html", "") + 'page-' + str(i) + '.html'
                    print(url_page)
                    response = requests.get(url_page)
                    if response.ok:
                        soup = BeautifulSoup(response.text, 'lxml')

                        livre = soup.findAll('article')

                        # Je crée une liste composées des urls de tous les livres d'une catégorie
                        for article in livre:
                            a = article.find('a')
                            link = a['href']
                            links.append('http://books.toscrape.com/catalogue/' + link[9:])

                # Je crée un fichier 'urls_livres.txt' qui regroupe tous les liens obtenus précèdement en vue de le réutiliser juste en dessous
                with open('urls_livres.txt', 'w') as file:
                    for link in links:
                        file.write(link + '\n')

                # J'utilise le fichier 'urls_livres.txt' en lecture comme fichier d'entrée pour la suite du script
                with open('urls_livres.txt', 'r') as inf:
                    # Je crée le fichier 'bouquin.csv' comme sortie finale regroupant toutes les informations de tous les livres d'une catégorie de livres
                    with open('bouquin.csv', 'w', encoding="utf8") as outf:
                        outf.write('upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating\n')
                        # J'itère dans le fichier 'urls_livres.txt' pour aller chercher les informations de tous les livres de chaque catégorie
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

            # Si j'ai qu'une page au sein d'une catégorie, je fais ça:
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
                with open("bouqin.csv'", 'w', encoding="utf8") as outf:
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

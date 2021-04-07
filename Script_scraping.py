import requests
from bs4 import BeautifulSoup
from math import *
import os
import re

"""
def imagedown(url, folder):
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except:
        pass
    os.chdir(os.mkdir(os.path.join(os.getcwd(), folder))
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all('img')
    for image in images:
        name = image['alt']
        link = 'http://books.toscrape.com/' + soup.find('img')['src']
        with open(name.replace(' ', '_') + '.jpg', 'wb') as f:
            im = requests.get(image_url)
            f.write(im.content)
            print('writing:', name)
"""
def data_book_extraction(response): # permet d'extraire toutes les données pour un livre, de les enregistrer dans un fichier '.csv' par catégorie de livre et d'enregistrer chaque image
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        livre = soup.findAll('article')
        # Je crée une liste composées des urls de tous les livres d'une catégorie
        for article in livre:
            a = article.find('a')
            link = a['href']
            links_books_by_category.append('http://books.toscrape.com/catalogue/' + link[9:])

    # J'utilise le dictionnaire 'links_books_by_category' pour la suite du script
    # Je crée le fichier 'catégorie.csv' (à chaque catégorie son fichier) comme sortie finale regroupant toutes les informations de tous les livres d'une catégorie de livres
    with open('Data/' + key + '.csv', 'w', encoding="utf8") as outf:
        outf.write('upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating\n')

        for el in links_books_by_category:
            url = el.strip()
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
                image_url = 'http://books.toscrape.com/' + soup.find('img')['src']
                outf.write(universal_product_code + ',' + title + ',' + price_including_tax + ',' + price_excluding_tax + ',' + number_available + ',' + product_description.replace(',', '') + ',' + category + ',' + review_rating + image_url + '\n')
                # supprime les caractères spéciaux
                title = re.sub("\W+", "_", title)
                title = title.strip()
                with open('Data/' + title.replace(' ', '_') + '.jpg', 'wb') as f:
                    im = requests.get(image_url)
                    f.write(im.content)
                    print('writing:', title)

url = 'http://books.toscrape.com/index.html'
response = requests.get(url) #j'obtiens le contenu de l'url passée en paramètre
soup = BeautifulSoup(response.text, 'lxml') #je parse le contenu à l'aide de BeautifulSoup et du parseur 'lxml'
categories = {}
livres = {}

# Je crée une liste 'categories' regroupant les urls de chaque catégorie
find_all_a = soup.find('div', class_='side_categories').find('ul').find_next('ul').find_all(href=True)
for el in find_all_a:
    name = el.text.strip()
    print(name)
    categories[name] = 'http://books.toscrape.com/' + el['href']
    print('http://books.toscrape.com/' + el['href'])

for key in categories:
    print(key,': ', categories[key])

# J'itère dans ma liste 'categories' fraichement créée pour aller chercher les adresses des catégories
for key in categories:
    url_category = categories[key]
    response = requests.get(url_category)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        #Je veux connaître le nombre de livres total dans la catégorie car je sais qu'il n'y a que 20 livres par page et cela me permet d'en déduire le nombre de pages dans la variable : "pages_number"
        books_number = soup.find('form', {'class': 'form-horizontal'}).find('strong')
        pages_number = ceil(int(books_number.text) / int(20))
        print('Ci-desssous les livres de la catégorie:!!!!!!!!!!!!!!!!!!!!!' + key + '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('Nombre de pages: ', pages_number)

        # Si j'ai plusieurs page au sein d'une catégorie, je fais ça pour naviguer au sein des pages et obtenir l'URL de chaque livre:
        if pages_number > 1:
            links_books_by_category = []
            for i in range(1,pages_number+1): #J'itère au sein des page avec une boucle for
                url_page = url_category.replace("index.html", "") + 'page-' + str(i) + '.html'
                print(url_page)
                response = requests.get(url_page)
                data_book_extraction(response)
                links_books_by_category = []

        # Si j'ai qu'une page au sein d'une catégorie, je fais ça:
        else:
            links_books_by_category = []
            print(url_category)
            response = requests.get(url_category)
            data_book_extraction(response)









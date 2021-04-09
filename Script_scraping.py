import requests
from bs4 import BeautifulSoup
from math import *
import re
import os


# ************************************************************************---> FUNCTIONS USED <---************************************************************************ #


def urls_books_by_category(response): # permet d'obtenir la liste de tous les url des livres pour une catégorie

    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        livre = soup.findAll('article')
        # création d'une liste composées des urls de tous les livres d'une catégorie

        for article in livre:
            a = article.find('a')
            link = a['href']
            links_books_by_category.append('http://books.toscrape.com/catalogue/' + link[9:])
        return links_books_by_category

def book_image_saving(title,image_url): # permet de sauvegarder l'image d'un livre dans un fichier 'Datas' qui se trouve dans le répértoire du projet

    title = title.strip()  # la méthode '.strip()' permet de supprimer les espaces en début et fin de variable de type 'string'
    title = re.sub("\W+", "_", title)  # supprime les caractères spéciaux contenus dans les titres de livre

    with open('Datas/' + title.replace(' ', '_') + '.jpg', 'wb') as f:

        im = requests.get(image_url)
        f.write(im.content)
        print('writing:', title)


def book_datas_writing(key,links_books_by_category): # permet de créer un fichier '.csv' (à chaque catégorie son fichier) en sortie regroupant toutes les informations de tous les livres d'une catégorie de livres
        with open('Datas/' + key + '.csv', 'w', encoding="utf8") as outf: # création du fichier de sortie en '.csv'
            outf.write('upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating\n')
            i = 1 # cela va me permettre de rajouter au titre du livre son numéro pour identifier sa position au sein de la catégorie et le rendre unique
            for el in links_books_by_category: # itération au sein de la liste d'url de chaque catégorie

                url = el.strip()
                response = requests.get(url)

                if response.ok:
                    soup = BeautifulSoup(response.text, 'lxml')

                    universal_product_code = soup.find('td').text
                    title = soup.find('h1').text
                    title = title
                    price_including_tax = soup.find('th', text='Price (incl. tax)').find_next('td').text[1:]
                    price_excluding_tax = soup.find('th', text='Price (excl. tax)').find_next('td').text[1:]
                    number_available = soup.find('th', text='Availability').find_next('td').text
                    product_description = soup.find('h2').find_next().text
                    category = soup.find('a').find_next('a').find_next('a').find_next('a').text
                    review_rating = soup.find('p', class_='star-rating')['class'][1]
                    image_url = 'http://books.toscrape.com/' + soup.find('img')['src']
                    outf.write(universal_product_code + ',' + title + ',' + price_including_tax + ',' + price_excluding_tax + ',' + number_available + ',' + product_description.replace(',', '') + ',' + category + ',' + review_rating + image_url + '\n')

                    title = title[:75] + (title[75:] and '...') # permet de limiter la longueur des titres
                    title = str(i) + '_' + title + '_' + key # j'ajoute la catégorie au titre pour pouvoir distinguer les titres qui auraient le meme nom mais qui appartiennent à différentes catégories
                    book_image_saving(title,image_url) # utilisation de la fonction pour enregistrer l'image correspondante du livre
                    i += 1

def categories_url_listing(soup): # permet de créer une liste 'categories' regroupant les urls de chaque catégorie

    find_all_a = soup.find('div', class_='side_categories').find('ul').find_next('ul').find_all(href=True)
    for el in find_all_a:
        name = el.text.strip()
        categories[name] = 'http://books.toscrape.com/' + el['href']


# ************************************************************************---> SCRIPT <---************************************************************************ #


url = 'http://books.toscrape.com/index.html'
response = requests.get(url) # permet d'obtenir le contenu de l'url passée en paramètre
soup = BeautifulSoup(response.text, 'lxml') # permet de parser le contenu à l'aide de BeautifulSoup et du parseur 'lxml'
categories = {}
categories_url_listing(soup) # utilisation de cette fonction pour obtenir une liste des urls pour chaque catégorie de livre
os.mkdir('Datas') # permet de créer le répérértoire 'Datas' qui va accueillir les fichiers CSV et les images

for key in categories: # itérations dans la liste 'categories' elle même fournie par la fonction 'categories_url_listing' pour aller chercher les adresses des catégories

    url_category = categories[key]
    response = requests.get(url_category)

    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')

        books_number = soup.find('form', {'class': 'form-horizontal'}).find('strong') # permet de connaître le nombre de livres total dans la catégorie car je sais qu'il n'y a que 20 livres par page et cela me permet d'en déduire le nombre de pages dans la variable : "pages_number"
        pages_number = ceil(int(books_number.text) / int(20))
        print('Ci-desssous les livres de la catégorie:************************!!!!!!!!!!!!!!!!!!!!!!!!!!!!' + key + '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!***********************************')
        print('Nombre de pages: ', pages_number)

        if pages_number > 1: # si il y a plusieurs page au sein d'une catégorie, le script pagine pour obtenir l'URL de chaque livre:

            links_books_by_category = [] # utilisation du dictionnaire 'links_books_by_category' pour la suite du script

            for i in range(1,pages_number+1): # itération au sein des page avec une boucle for

                url_page = url_category.replace("index.html", "") + 'page-' + str(i) + '.html'
                print('lien de la page', i,':',url_page)
                response = requests.get(url_page)
                urls_books_by_category(response)

            book_datas_writing(key,links_books_by_category)


        else: # Sinon le script prend directement l'url de l'unique page existante comme entrée

            links_books_by_category = []
            print('lien de la page :',url_category)
            response = requests.get(url_category)
            urls_books_by_category(response)
            book_datas_writing(key,links_books_by_category)

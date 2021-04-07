import requests
from bs4 import BeautifulSoup

links = []

url = 'http://books.toscrape.com/catalogue/sharp-objects_997/index.html'
response = requests.get(url)

with open('bouquin.csv', 'w', encoding="utf8") as outf:
    outf.write('upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating\n')

    product_page_url = url
    print('URL :', product_page_url)

    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')

        universal_product_code = soup.find('td').text
        print('UPC :', universal_product_code)

        title = soup.find('h1').text
        print('Title :', title)

        price_including_tax = soup.find('th', text = 'Price (incl. tax)').find_next('td').text[1:]
        print('Price including tax :', price_including_tax)

        price_excluding_tax = soup.find('th', text = 'Price (excl. tax)').find_next('td').text[1:]
        print('Price excluding tax :', price_excluding_tax)

        number_available = soup.find('th', text='Availability').find_next('td').text
        print('Number available :', number_available)

        product_description = soup.find('h2').find_next().text
        print('Product description :', product_description)

        category = soup.find('a').find_next('a').find_next('a').find_next('a').text
        print('Category :', category)

        review_rating = soup.find('p', class_= 'star-rating')['class'][1]
        print('review_rating :', review_rating)

        image_url = soup.find('img')['src']
        print('Image_URL :', image_url)

        outf.write(universal_product_code + ',' + title + ',' + price_including_tax + ',' + price_excluding_tax + ',' + number_available + ',' + product_description.replace(',','') + ',' + category + ',' + review_rating + ',' + image_url)

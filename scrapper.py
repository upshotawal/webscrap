from email import header
import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = "https://www.sastodeal.com/"

product_titles = []
product_img_links = []
product_ratings = []
product_description = []
product_price = []
product_shdescrip = []

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"

}


productlinks = []
for x in range(1, 6):
    r = requests.get(
        f'https://www.sastodeal.com/home-and-living/fitness-health-care/gym-exercise-accessories.html?p={x}')
    soup = BeautifulSoup(r.content, 'lxml')
    productlist = soup.find_all('li', class_='item product product-item')
    for item in productlist:
        for link in item.find_all('a', {'class': 'product photo product-item-photo'}, href=True):
            productlinks.append(link['href'])


for link in productlinks:

    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    try:
        name = soup.find('span', class_='base').text.strip()
    except:
        name = 'no name'

    try:
        images = []
        for img in soup.findAll('img'):
            images.append(img.get('src'))
    except:
        images = 'no images'

    try:
        price = soup.find('span', class_='price').text.strip()
    except:
        price = 'no price'
    try:
        description = soup.find('div', class_='value').text.strip()
    except:
        description = 'no description'
    try:
        rating = soup.find(
            'span', class_='product-overall-rating-summary').text.strip()
    except:
        rating = 'no rating'
    try:
        review = soup.find(
            'span', itemprop='reviewCount').text.strip()
    except:
        review = 'no review'

    product = {
        'name': name,
        'price': price,
        'description': description,
        'rating': rating,
        'review ': review,

    }
    productlist.append(product)
    print('Saving: ', product['name'])

df = pd.DataFrame(productlist)
df.to_csv('gym.csv')

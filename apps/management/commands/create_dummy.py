import os

import requests
from django.core.management import BaseCommand
from faker import Faker

from apps.models import Product, Store, Category

fake = Faker()


class Command(BaseCommand):
    help = '''
        You can create dummy data. Like this:
    * Products      -> 1000
    * Categories    -> 15
    * Store          -> 20
    '''

    def handle(self, *args, **options):

        # Create 10 dummy data Category
        print('\n\n\t\tCREATING Category')
        for i in range(10):
            title = ''.join(fake.text().split()[:3])
            print(title, end=' ')
            try:
                img = download_image(fake.image_url(), 'category')
            except:
                print('No answer')
                continue
            catagory = Category.objects.create(title=title, image=img)
            catagory.save()
            print('category added')

        # Create 20 dummy data Store
        print('\n\n\t\tCREATING Store')
        for i in range(20):
            name = fake.unique.company()
            print(name, end=' ')
            try:
                image = fake.unique.image_url()
            except:
                print('No answer')
                continue
            store = Store.objects.create(image=download_image(image, "store"), name=name,
                                         short_des=''.join(name.split()[:2]))
            print('store added')

        print('\n\n\t\tCREATING Product')
        # Create 1000 dummy data Product
        for i in range(10):
            title = ' '.join(fake.text().split()[:3])
            print(title, end=' ')
            # try:
            main_picture = download_image(fake.unique.image_url(), 'product')
            # except:
            #     print(os.error)
            #     print('No answer')
            #     continue
            price = abs(int(fake.longitude())) * 1000
            created_at = fake.date_time()
            bonus = price // 100
            free_delivery = fake.boolean()
            reserve = abs(int(fake.longitude()))
            store = 1
            category = 1
            product = Product.objects.create(title=title, main_picture=main_picture, price=price, created_at=created_at,
                                             bonus=bonus, free_delivery=free_delivery, reserve=reserve, store_id=store,
                                             category_id=category)
            print('product added')


def download_image(url, place_url):
    place_url = f'fake/{place_url}'
    if not os.path.exists(f'media/{place_url}'):
        os.makedirs(f'media/{place_url}')

    with open(f'media/{place_url}/{url.split("/")[-1]}.jpg', 'wb') as handle:
        response = requests.get(url, stream=True)
        if not response.ok:
            pass
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

    return place_url + '/' + url.split("/")[-1] + '.jpg'
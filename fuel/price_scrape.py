from datetime import date, timedelta
import re
import time 

from requests_html import HTMLSession
from .models import FuelPrice


def get_regular_info(url):
    time.sleep(0.5)
    session = HTMLSession()
    r = session.get(url)

    # アクセスに失敗したときの処理
    if r.status_code != 200:
        return None

    shop_name = r.html.find('.shop-header .title', first=True).text
    shop_name = convert_shop_name(shop_name)
    regular_info = r.html.find('.card', first=True)
    fuel_name = regular_info.find('.mode-label', first=True).text
    price = regular_info.find('.price', first=True).text
    days = int(re.search(r'\d*', regular_info.find('.date', first=True).text).group())
    registered_date = get_registered_date(days)
    return {'shop_name': shop_name, 'fuel_name': fuel_name, 'price': price, 'registered_date': registered_date}

def get_registered_date(days):
    today = date.today()
    registered_date =  today - timedelta(days=days)
    return registered_date


def convert_shop_name(shop_name):
    if 'PLANT' in shop_name:
        shop_name = 'PLANT3 川北店'
    if 'カナショク' in shop_name:
        shop_name = 'カナショク 寺井店'
    return shop_name


def scrape_fuel_price(urls):
    data = []
    for url in urls:
        data.append(get_regular_info(url))
    return data


def is_insert_data(data):
    shop_name = data['shop_name']
    registered_date = data['registered_date']
    latest_data_date = FuelPrice.objects.filter(place=shop_name).latest('acquisition_date').confirmed_date
    if latest_data_date != registered_date:
        print(latest_data_date, registered_date)
        return True
    else:
        print(False, latest_data_date, registered_date)
        return False


def insert_data(data):
    fuel_price = FuelPrice(place=data['shop_name'], price=data['price'], confirmed_date=data['registered_date'])
    fuel_price.save()


if __name__ == '__main__':
    urls = ['https://gogo.gs/shop/1799000108', 'https://gogo.gs/shop/1799000017']
    data = scrape_fuel_price(urls)
    # is_insert_data(data[0])
    print(data)

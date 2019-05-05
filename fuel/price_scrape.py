from datetime import datetime
import time

from requests_html import HTMLSession
from .models import FuelPrice
from django.utils import timezone


def get_regular_info(url):
    session = HTMLSession()
    r = session.get(url)

    # アクセスに失敗したときの処理
    if r.status_code != 200:
        return None

    shop_name = r.html.find('.shop-header .title', first=True).text
    shop_name = convert_shop_name(shop_name)
    price_history_table = r.html.find('.table-bordered', first=True)
    price_history_data = []
    columns_name = list(map(lambda th: th.text, price_history_table.find('tr', first=True).find('th')))
    rows = price_history_table.find('tr')[1:]
    for row in rows:
        data = {'店名': shop_name}
        if len(row.find('td')) < 6:
            continue
        for i, (key, value) in enumerate(zip(columns_name, row.find('td'))):
            if i == 0:
                data[key[:4]] = get_registered_date(value)
                continue
            data[key] = value.text
        price_history_data.append(data)
    return price_history_data[0]


def get_registered_date(td_html):
    registered_date = td_html.find('.entrydate')[0].text[4:]
    registered_date = str(timezone.now().year) + '/' + registered_date
    # registered_date = str(datetime.now().year) + '/' + registered_date
    return datetime.strptime(registered_date, "%Y/%m/%d %H:%M:%S")


def convert_shop_name(shop_name):
    if 'PLANT' in shop_name:
        shop_name = 'PLANT3 川北店'
    if 'カナショク' in shop_name:
        shop_name = 'カナショク 寺井店'
    return shop_name


def scrape_fuel_price(urls):
    return [get_regular_info(url) for url in urls]


def is_insert_data(data):
    shop_name = data['店名']
    registered_date = data['確認日時']
    latest_data_date = FuelPrice.objects.filter(place=shop_name).latest('acquisition_date').confirmed_date
    if latest_data_date != registered_date.date():
        print(True, latest_data_date, registered_date.date())
        return True
    else:
        print(False, latest_data_date, registered_date.date())
        return False


def insert_data(data):
    fuel_price = FuelPrice(place=data['店名'], price=data['レギュラー'], confirmed_date=data['確認日時'])
    fuel_price.save()


if __name__ == '__main__':
    urls = ['https://gogo.gs/shop/1799000108', 'https://gogo.gs/shop/1799000017']
    data = scrape_fuel_price(urls)
    print(is_insert_data(data[0]))

from django.core.management import BaseCommand

from fuel.models import FuelPrice
import fuel.price_scrape as scrape

class Command(BaseCommand):
    help = 'gogo.gsからPLANTとカナショクのガソリン価格を取得'

    def handle(self, *args, **options):
        urls = ['https://gogo.gs/shop/1799000108', 'https://gogo.gs/shop/1799000017']
        latest_data = []
        shops_data = scrape.scrape_fuel_price(urls)
        for shop_data in shops_data:
            if scrape.is_insert_data(shop_data):
                scrape.insert_data(shop_data)
            latest_data.append(FuelPrice.objects.filter(place=shop_data['店名']).latest('acquisition_date'))
        self.stdout.write(self.style.SUCCESS('Hello Django Command!'))

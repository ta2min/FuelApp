from django.db import models
from django.utils import timezone


class Refueling(models.Model):
    place = models.CharField('ガソリンスタンド名', max_length=20, default='プラント3 川北店')
    price = models.IntegerField('価格')
    total = models.IntegerField('合計', default=0)
    amount = models.FloatField('給油量')
    refueling_date = models.DateField('給油日', default=timezone.now)
    trip_meter = models.FloatField('トリップメータ', null=True)
    created_date = models.DateTimeField('作成日時', auto_now_add=True)
    
    def __str__(self):
        return str(self.id)


class FuelPrice(models.Model):
    place = models.CharField('ガソリンスタンド名', max_length=20)
    price = models.IntegerField('価格')
    confirmed_date = models.DateField('価格を確認した日')
    acquisition_date = models.DateTimeField('取得日', auto_now_add=True)

    def __str__(self):
        return self.confirmed_date.strftime('%Y-%m-%d') + self.place
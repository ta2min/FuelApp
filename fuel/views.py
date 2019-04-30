from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse

from .models import Refueling, FuelPrice
from .forms import RefuelingForm
from .price_scrape import scrape_fuel_price, is_insert_data, insert_data


def list(request):
    title = '給油履歴'

    # ガソリン価格の最新情報を取得
    plant3_data = FuelPrice.objects.filter(place='PLANT3 川北店').latest('acquisition_date')
    kanasyoku_data =  FuelPrice.objects.filter(place='カナショク 寺井店').latest('acquisition_date')

    # 給油履歴の取得
    refueling_logs =  Refueling.objects.order_by('-refueling_date')

    return TemplateResponse(request, 'fuel/list.html',
                            {'title': title,
                             'plant3_data': plant3_data,
                             'kanasyoku_data': kanasyoku_data,
                             'refueling_logs': refueling_logs})


def detail(request):
    pass


def refueling_edit(request, refueling_id=None):
    # GETリクエストのときはrefueling_idがあれば修正、なければ追加の編集画面を返す
    if refueling_id:
        refueling = get_object_or_404(Refueling, pk=refueling_id)
    else:
        refueling = Refueling()

    if request.method == 'POST':
        form = RefuelingForm(request.POST, instance=refueling)
        if form.is_valid():
            refueling = form.save(commit=False)
            refueling.save()
            return redirect('list')
    else:
        form = RefuelingForm(instance=refueling)

    return TemplateResponse(request, 'fuel/edit.html',
                            {'form': form,
                             'refueling_id': refueling_id})


def delete(request, refueling_id):
    refueling = get_object_or_404(Refueling, pk=refueling_id)
    refueling.delete()
    return redirect('list')


def fuel_price(request):
    urls = ['https://gogo.gs/shop/1799000108', 'https://gogo.gs/shop/1799000017']
    latest_data = []
    shops_data = scrape_fuel_price(urls)
    for shop_data in shops_data:
        if is_insert_data(shop_data):
            insert_data(shop_data)
        latest_data.append(FuelPrice.objects.filter(place=shop_data['shop_name']).latest('acquisition_date'))
    return render(request, 'fuel/fuel_price.html',
            {'latest_data': latest_data})

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    CreateView,
    # DeleteView,
    ListView,
    UpdateView,
    View,
)
from .models import Refueling, FuelPrice
from .forms import RefuelingForm
from .price_scrape import scrape_fuel_price, is_insert_data, insert_data


class RefuelingList(ListView):
    model = Refueling
    context_object_name = 'refueling_logs'
    paginate_by = 100
    template_name = 'fuel/fuel_list.html'

    def get_queryset(self):
        return Refueling.objects.order_by('-refueling_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plant3_data'] = FuelPrice.objects.filter(place='PLANT3 川北店').latest('acquisition_date')
        context['kanasyoku_data'] = FuelPrice.objects.filter(place='カナショク 寺井店').latest('acquisition_date')
        return context


class RefuelingAdd(CreateView):
    model = Refueling
    form_class = RefuelingForm
    template_name = 'fuel/edit.html'
    success_url = '/fuel'


class RefuelingMod(UpdateView):
    model = Refueling
    form_class = RefuelingForm
    template_name = 'fuel/edit.html'
    success_url = '/fuel'


class RefuelingDelete(View):
    def get(self, request, **kwargs):
        refueling = get_object_or_404(Refueling, pk=self.kwargs['pk'])
        refueling.delete()
        return redirect('refueling_list')


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

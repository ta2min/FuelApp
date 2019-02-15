from django.forms import ModelForm
from .models import Refueling


class RefuelingForm(ModelForm):
    """給油登録フォーム"""
    class Meta:
        model = Refueling
        fields = ('refueling_date', 'place', 'price', 'amount', 'total', 'trip_meter')
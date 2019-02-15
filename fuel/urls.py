from django.urls import path

from . import views


urlpatterns = [
    path('', views.list, name='list'),
    path('add/', views.refueling_edit, name='refueling_add'),
    path('detail/<int:refueling_id>/', views.detail, name='detail'),
    path('mod/<int:refueling_id>/', views.refueling_edit, name='refueling_mod'),
    path('delete/<int:refueling_id>/', views.delete, name='delete'),
    path('price/', views.fuel_price, name='fuel_price')
]
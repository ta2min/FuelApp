from django.urls import path

from . import views

urlpatterns = [
    path('', views.RefuelingList.as_view(), name='refueling_list'),
    path('delete/<int:pk>/', views.RefuelingDelete.as_view() , name='refueling_delete'),
    path('price/', views.fuel_price, name='fuel_price'),
    path('add/', views.RefuelingAdd.as_view(), name="refueling_add"),
    path('update/<int:pk>/', views.RefuelingMod.as_view(), name='refueling_update'),
]
from django.urls import path
from . import views

app_name = 'dietapp'
urlpatterns = [
	path('', views.index, name='index'),
	path('product/<int:product_id>/', views.product_info, name='product'),
	path('result/', views.result, name='result')
]

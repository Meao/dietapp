from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Product, Diet
from .optimization import optimize_min

# Названия views соответвтуют названиям страниц, к которым переходим с помощью алгоритма

def index(request):
	product_list = Product.objects.order_by('name')

	context = {
		'product_list': product_list,
	}

	return render(request, 'dietapp/index.html', context)

def product_info(request, product_id):
	product = Product.objects.get(id=product_id)
	context = {'product': product}

	return render(request, 'dietapp/product_detail.html', context)

def result(request):
	product_list = Product.objects.order_by('name')
	selected_product_list = Product.objects.filter(pk__in = \
								request.POST.getlist('product'))

	opt = optimize_min(selected_product_list)

	result_dict = dict(zip(selected_product_list, opt))
	context = {
		'product_list': product_list,
		'result_dict': result_dict,
		# 'opt': opt,
	}
	return render(request, 'dietapp/index.html', context)

	#return HttpResponseRedirect(reverse('dietapp:result'))

import numpy
# from .linprog_optimisation import calcul
from .my_optimisation import app_products2optimisation
import time

def optimize_min(selected_product_list):
	result = app_products2optimisation(selected_product_list)
	# result = calcul(selected_product_list)
	return result

from django.apps import AppConfig
from django.db.models.signals import post_save
#from dietapp.signals import save_product
#from dietapp.models import Product


class DietappConfig(AppConfig):
	name = 'dietapp'
	
#	def ready(self):
#		post_save.connect(save_product, sender = Product)

from .models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender = Product)
def save_product(sender, instance, **kwargs):
	print("Product created")
	instance.product.save()
	
#post_save.connnect(save_product, sender = Product)

from django.db import models
#from django.db.models.signals import post_save
#from django.dispatch import receiver

# Создана модель под существующую задачу.

class Product(models.Model):
	name = models.CharField(max_length = 100)
	fat = models.IntegerField(default = 0)
	calories = models.IntegerField(default = 0)
	default_price = models.IntegerField(default = 0)
	proteins = models.IntegerField(default = 0)
	hydrocarbons = models.IntegerField(default = 0)
	minerals = models.IntegerField(default = 0)
	calcuim_qty = models.IntegerField(default = 0)
	vit_a_qty = models.IntegerField(default = 0)

	def __str__(self):
		return self.name

	# default_size = models.IntegerField(default = 1000) # in grams, cannot be 0
	# def getDefaultSize(self):
		# return self.default_size


class Diet(models.Model):
	name = models.CharField(max_length = 100)
	products = models.ManyToManyField(Product)

	def __str__(self):
		return self.name

	#def calories() # count calories in diet

# class Portion(models.Model):
	# product = models.ForeignKey(Product, on_delete=models.CASCADE)
	# size = models.IntegerField(default = 123) # in grams

	# def __str__(self):
		# return f"{self.size}g {self.product.name}"

	# def calories(self):
		# assert self.product.default_size != 0, f"ERR: product {product} calories cannot be zero."
		# return self.product.calories * (self.size / self.product.default_size)




# @receiver(post_save, sender = Product)
# def save_product(sender, instance, **kwargs):
	# print(sender.objects.all())

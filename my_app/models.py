from django.db import models
from accounts.models import User
# from django.contrib.auth.models import User

class Product(models.Model):
	product_name = models.CharField(max_length = 200)
	product_compound = models.TextField()
	product_price = models.FloatField()
	product_image = models.ImageField(upload_to = 'image/')

	def __str__(self):
		return self.product_name  


class Coment(models.Model):
	username = models.CharField(max_length = 150)         
	phone = models.CharField(max_length = 20)
	email = models.CharField(max_length = 50)
	message = models.TextField()
	date = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return f'{self.username}'


# 1- bosqich 

# order yaniy mahsulotmi savatga qushish uchun model
# from django.contrib.auth.models import User

class Order(models.Model):
	customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank = True, null = True)
	data_ordered = models.DateTimeField(auto_now_add = True)
	name = models.CharField(max_length = 200, null = True)
	complete = models.BooleanField(default = False, null = True, blank = False)

	"""pastdagi quantity(mahsulotlarni sonini) va 
	barcha orderItem(savatdagi mahsulotlar)ni hisoblash uchun"""
	@property #Dekorator
	def get_card_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total	

	"""pastdagi get_total funksiyadan aytgan qiymatni barcha orderItem
	(savatdagi mahsulotlar) larni husoblaash uchun"""
	@property # Dekorator
	def get_card_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	#String obyektini qaytaradi
	def __str__(self):
		return str(self.id)


# Mahsulotni qachon ba kim tomonidan qaysi qushilhanligini saqlash uchun model
class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete = models.SET_NULL, blank = True, null = True)
	order = models.ForeignKey(Order, on_delete = models.SET_NULL, blank = True, null = True)
	quantity = models.IntegerField(default = 0, null = True, blank = True)
	data_added = models.DateTimeField(auto_now_add = True)

	#mahsulot narxni soniga kopaytirib beradi
	@property #Dekorator
	def get_total(self):
		total = self.product.product_price * self.quantity
		return total

	# String obyektini qaytaradi
	def __str__(self):
		return str(self.id)
	


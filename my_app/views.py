from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from .models import *
import requests 
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from django.http import JsonResponse
import json

def homePageView(request):
	if request.user.is_authenticated:
		mahsulot = Product.objects.all()
		customer = request.user
		order, created = Order.objects.get_or_create(customer = customer, complete = False)
		items = order.orderitem_set.all()
		cartItems = order.get_card_items # savatdagi mahsulot soni 

		context = { 
		"mahsulotlar" : mahsulot,
		"cartItems" : cartItems
		}
		return render (request, 'index.html', context)
	else:
		mahsulot = Product.objects.all()
		items = []
		order = { ' get_cart_total': 0 , 'get_card_items': 0}
		cartItems = order['get_card_items']
		context = {
		'mahsulotlar' : mahsulot,
		'cartItems' : cartItems
		}
		return render(request, 'index.html', context)

def aboutPageView(request):
		if request.user.is_authenticated:
			mahsulot = Product.objects.all()
			customer = request.user
			order, created = Order.objects.get_or_create(customer = customer, complete = False)
			items = order.orderitem_set.all()
			cartItems = order.get_card_items # savatdagi mahsulot soni 

			context = { 
			"mahsulotlar" : mahsulot,
			"cartItems" : cartItems
			}
			return render (request, 'index.html', context)
		else:
			items = []
			order = { ' get_cart_total': 0 , 'get_card_items': 0}
			cartItems = order['get_card_items']
			context = {
			'cartItems' : cartItems
			}
			return render(request, 'about.html', context)
	

def menuPageView(request):
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer = customer, complete = False)
		items = order.orderitem_set.all()
		cartItems = order.get_card_items # savatdagi mahsulotlar soni
	else:
		items = []
		order = {'get_card_total': 0, "get_card_items": 0}
		cartItems = order['get_card_items'] # qaysi funksiya orqali hisoblasin

	obj = Product.objects.all()
	page_n = request.GET.get('page', 1)
	p = Paginator(obj, 2)
	try:
		page = p.page(page_n)
	except Exception:
		page = p.page(1)
	context = {
	'page': page,
	'cartItems': cartItems
	}
	return render(request, 'menu.html', context)


# Mahsulotlarni qushishni bajarish uchun funsiya yozamiz

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Bosildi: ',action) #terminalda mahsulot ID si ko'rinishi kerak
	print('Mahsulot IDsi: ',productId)

	# keyingi uzgarish POST create qilish
	# base.html dagi savat iconi ga  mahsulot soni korsatishimiz kerak
	customer = request.user
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer,complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	
	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)
	# ushbu funksiyaga url yasashimiz kerak

def cart(request):
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_card_items
	else:
		# reverse_lazy('login')
		items = []
		order = {'get_cart_total': 0, "get_card_items": 0}
		cartItems = order['get_card_items']

	context = {"items": items,"order": order,'cartItems':cartItems }
	return render(request, 'cart.html', context)
	# ushbu funksiyaga url yasashimiz kerak
	# base html dagi savat urliga cart ni belgilab quyishimiz kerak


def telegram_bot_sendtext(bot_message):
	bot_token = '2085755410:AAH6uMRybPrJtOrcGLuRmgvyCEL6-FGNACU'
	bot_ChatId = '913748839'
	send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_ChatId + "&parse_mode=Markdown&text= " + bot_message
	response = requests.get(send_text)
	return response.json()



def bookPageView(request):
		if request.user.is_authenticated:
			if request.method == 'POST':
				name = request.POST.get('name', None)
				phone = request.POST.get('phone', None)
				email = request.POST.get('email', None)
				message = request.POST.get('message', None)
				user = Coment.objects.create(
					username = name,
					phone = phone,
					email = email,
					message = message
				)
				user.save()
				telegram_bot_sendtext(f"Ismi: {user} \nPhone:{phone} \nEmail:{email} Message:{message} ")

			mahsulot = Product.objects.all()
			customer = request.user
			order, created = Order.objects.get_or_create(customer = customer, complete = False)
			items = order.orderitem_set.all()
			cartItems = order.get_card_items # savatdagi mahsulot soni 

			context = { 
			"mahsulotlar" : mahsulot,
			"cartItems" : cartItems
			}
			return render (request, 'book.html', context)
		else:
			if request.method == 'POST':
				name = request.POST.get('name', None)
				phone = request.POST.get('phone', None)
				email = request.POST.get('email', None)
				message = request.POST.get('message', None)
				user = Coment.objects.create(
					username = name,
					phone = phone,
					email = email,
					message = message
					)
				user.save()
				telegram_bot_sendtext(f"Ismi: {user} \nPhone:{phone} \nEmail:{email} Message:{message} ")
			context = {}
			return render(request, 'book.html', context)

	

class ProductCreateView(CreateView):
	model = Product
	template_name = 'product_create.html'
	# bu qolda qowiw fields = ('mahsulot_nomi', 'mahsulot_tarkibi','mahsulot_rasmi','mahsulot_narxi')
	fields = '__all__'
	success_url = reverse_lazy('index')


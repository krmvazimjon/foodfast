from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	path('',homePageView, name = 'index'),
	path('menu/', views.menuPageView, name = 'menu'),
	path('aboutus/', aboutPageView, name = 'about'),
	path('book/', bookPageView, name = 'book'),
	path('product_create/', ProductCreateView.as_view(), name = 'product_create'),
	path('update_item/', views.updateItem),
	# cart funsiyasi uchun 
	path('cart/', views.cart, name= "cart"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
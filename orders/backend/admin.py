from django.contrib import admin
from models import Product, Category, Order, OrderItem, User, Shop
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'image')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
from django.urls import path
from .views import PartnerUpdate, LoginView, RegistrationView, ProductListView, CartView, ContactView, OrderConfirmationView, OrderHistoryView


urlpatterns = [
    path('partner/update/', PartnerUpdate.as_view(), name='partner-update'),
    path('login/', LoginView.as_view(), name='login'),
     path('register/', RegistrationView.as_view(), name='register'),
     path('products/', ProductListView.as_view(), name='product-list'),
     path('cart/', CartView.as_view(), name='cart'),
     path('contacts/', ContactView.as_view(), name='contacts'),
     path('order/confirm/', OrderConfirmationView.as_view(), name='order-confirm'),
     path('orders/history/', OrderHistoryView.as_view(), name='order-history'),
]

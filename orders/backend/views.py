from django.http import JsonResponse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views import View
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from requests import get
from yaml import load as load_yaml, Loader
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, Contact


User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class PartnerUpdate(View):
    """
    Класс для обновления прайса от поставщика
    """
    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        # if request.user.type != 'shop':
        #     return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        url = request.data.get('url')
        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return JsonResponse({'Status': False, 'Error': str(e)})
            else:
                stream = get(url).content

                data = load_yaml(stream, Loader=Loader)

                shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)
                for category in data['categories']:
                    category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                    category_object.shops.add(shop.id)
                    category_object.save()
                ProductInfo.objects.filter(shop_id=shop.id).delete()
                for item in data['goods']:
                    product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

                    product_info = ProductInfo.objects.create(product_id=product.id,
                                                              external_id=item['id'],
                                                              model=item['model'],
                                                              price=item['price'],
                                                              price_rrc=item['price_rrc'],
                                                              quantity=item['quantity'],
                                                              shop_id=shop.id)
                    for name, value in item['parameters'].items():
                        parameter_object, _ = Parameter.objects.get_or_create(name=name)
                        ProductParameter.objects.create(product_info_id=product_info.id,
                                                        parameter_id=parameter_object.id,
                                                        value=value)

                return JsonResponse({'Status': True})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

@method_decorator(csrf_exempt, name='dispatch')
class ProductListView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        product_list = []
        for product in products:
            product_list.append({
                'name': product.name,
                'description': product.description,
                'supplier': product.supplier.name,
                'price': product.price,
                'quantity': product.quantity,
            })
        return JsonResponse({'products': product_list})
    

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'Status': True})
        else:
            return JsonResponse({'Status': False, 'Errors': 'Неверный email или пароль'})
        


@method_decorator(csrf_exempt, name='dispatch')
class RegistrationView(View):
    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not (first_name and last_name and email and password):
            return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

        try:
            User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        except Exception as e:
            return JsonResponse({'Status': False, 'Errors': str(e)})

        return JsonResponse({'Status': True})


class ProductListView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        product_list = []
        for product in products:
            product_list.append({
                'name': product.name,
                'description': product.description,
                'supplier': product.supplier.name,
                'price': product.price,
                'quantity': product.quantity,
            })
        return JsonResponse({'products': product_list})
    
class CartView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        cart, _ = Order.objects.get_or_create(user=request.user, status='basket')
        cart_items = OrderItem.objects.filter(order=cart)
        items_list = []
        for item in cart_items:
            items_list.append({
                'product_name': item.product_info.product.name,
                'shop': item.product_info.shop.name,
                'price': item.product_info.price,
                'quantity': item.quantity,
                'total': item.quantity * item.product_info.price,
            })
        return JsonResponse({'cart': items_list})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        product_info_id = request.POST.get('product_info_id')
        quantity = request.POST.get('quantity')

        if not (product_info_id and quantity):
            return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

        cart, _ = Order.objects.get_or_create(user=request.user, status='basket')
        OrderItem.objects.create(order=cart, product_info_id=product_info_id, quantity=quantity)

        return JsonResponse({'Status': True})

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        item_id = request.POST.get('item_id')

        if not item_id:
            return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

        cart, _ = Order.objects.get_or_create(user=request.user, status='basket')
        OrderItem.objects.filter(order=cart, id=item_id).delete()

        return JsonResponse({'Status': True})
    
class ContactView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        contacts = Contact.objects.filter(user=request.user)
        contact_list = []
        for contact in contacts:
            contact_list.append({
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'email': contact.email,
                'phone': contact.phone,
                'address': contact.address,
                'city': contact.city,
                'street': contact.street,
                'house': contact.house,
                'structure': contact.structure,
                'building': contact.building,
                'apartment': contact.apartment,
            })
        return JsonResponse({'contacts': contact_list})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        street = request.POST.get('street')
        house = request.POST.get('house')
        structure = request.POST.get('structure')
        building = request.POST.get('building')
        apartment = request.POST.get('apartment')

        if not (first_name and last_name and email and phone and address and city and street):
            return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

        Contact.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            street=street,
            house=house,
            structure=structure,
            building=building,
            apartment=apartment,
        )

        return JsonResponse({'Status': True})

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        contact_id = request.POST.get('contact_id')

        if not contact_id:
            return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

        Contact.objects.filter(user=request.user, id=contact_id).delete()

        return JsonResponse({'Status': True})
    
class OrderConfirmationView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        cart_id = request.POST.get('cart_id')
        contact_id = request.POST.get('contact_id')

        if not (cart_id and contact_id):
            return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

        cart = Order.objects.get(id=cart_id, user=request.user, status='basket')
        cart.status = 'new'
        cart.contact_id = contact_id
        cart.save()

        return JsonResponse({'Status': True})
    
class OrderHistoryView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        orders = Order.objects.filter(user=request.user).exclude(status='basket')
        order_list = []
        for order in orders:
            order_list.append({
                'number': order.id,
                'date': order.dt,
                'total': sum(item.quantity * item.product_info.price for item in order.ordered_items.all()),
                'status': order.status,
            })
        return JsonResponse({'orders': order_list})
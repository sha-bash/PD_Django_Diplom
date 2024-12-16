from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from backend.models import Contact, Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, ConfirmEmailToken
from rest_framework.authtoken.models import Token

class RegisterAccountTests(APITestCase):
    def test_registration_success(self):
        url = reverse('backend:user-register')
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "StrongPassword123",
            "company": "Test Company",
            "position": "Test Position",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Check for 200 OK

    def test_registration_missing_fields(self):
        url = reverse('backend:user-register')
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data['Errors'])  
    def test_registration_weak_password(self):
        url = reverse('backend:user-register')
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "weak",  # Weak Password
            "company": "Test Company",
            "position": "Test Position",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data['Errors'])  # Check for password error

class LoginAccountTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='TestPassword123')

    def test_login_success(self):
        url = reverse('backend:user-login')
        data = {'email': 'testuser@example.com', 'password': 'TestPassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Token', response.data)  # Check for token in response

    def test_login_invalid_credentials(self):
        url = reverse('backend:user-login')
        data = {'email': 'testuser@example.com', 'password': 'IncorrectPassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Expecting 400 Bad Request
        self.assertIn('Errors', response.data)

class AccountDetailsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='TestPassword123')
        self.token = Token.objects.create(user=self.user)

    def test_get_account_details_authenticated(self):
        url = reverse('backend:user-details')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_get_account_details_unauthenticated(self):
        url = reverse('backend:user-details')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Expecting forbidden
        self.assertIn('Error', response.data)  # Check for error message

class ProductInfoViewTests(APITestCase):
    def setUp(self):
        self.shop = Shop.objects.create(name='Test Shop', state=True)
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', category=self.category)
        self.product_info = ProductInfo.objects.create(
            model='Test Model', external_id=123, product=self.product, shop=self.shop, quantity=10, price=100,
            price_rrc=120
        )

    def test_product_info_retrieval(self):
        url = reverse('backend:shops')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)  # Check data is returned

class ContactViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def test_create_contact(self):
        url = reverse('backend:user-contact')
        data = {'city': 'Test City', 'street': 'Test Street', 'phone': '+79999999999'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Assuming success is 200 OK
        self.assertIn('Status', response.data)  # Check for success status
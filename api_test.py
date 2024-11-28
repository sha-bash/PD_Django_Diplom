import requests
import json


base_url = 'http://localhost:8000/api/v1/'  

# Тестирование API для регистрации пользователя
response = requests.post(base_url + 'user/register', json={
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'johndo1e@example.ru',
    'password': 'password_123',
    'company': 'Example Company',
    'position': 'Example Position',
})
print('Тестирование API для регистрации пользователя')
print("Status Code:", response.status_code)
print("Response Text:", response.text)  # Это поможет увидеть, что возвращает сервер

# Тестирование API для авторизации пользователя
response = requests.post(base_url + 'user/login', json={
    'email': 'johndo1e@example.ru',
    'password': 'password_123'
})
print('Тестирование API для авторизации пользователя')
print("Login Response:", response.json())  # Должен вернуть сообщение об успехе с токеном

# Тестирование API для получения списка товаров
response = requests.get(base_url + 'products')
print('Тестирование API для получения списка товаров')
print("Products List Response:", response.json())  # Должен вернуть список товаров

# Тестирование API для получения спецификации товара
product_id = 1  
response = requests.get(base_url + f'products/{product_id}/')
print("Product Detail Status Code:", response.status_code)  # Проверка статуса ответа
print("Product Detail Response Text:", response.text)  # Вывод текста ответа

if response.status_code == 200:
    print("Product Detail Response JSON:", response.json())  # Если статус 200, выводим JSON
else:
    print(f"Error retrieving product detail: {response.status_code}, Response: {response.text}")# Должен вернуть спецификацию товара


# Авторизация пользователя
login_data = {
    'email': 'johndo1e@example.ru',
    'password': 'password_123'
}

login_response = requests.post(base_url + 'user/login', data=login_data)
print("Login Response:", login_response.json())

# Проверка успешной авторизации и получение токена
if login_response.status_code == 200:
    token = login_response.json().get('Token')
    headers = {'Authorization': f'Token {token}'}

    # Тестирование API для работы с корзиной (добавление товара)
    product_id = 1  
    response = requests.post(base_url + 'basket', headers=headers, json={
        'items': [{'product_info_id': product_id, 'quantity': 2}]
    })
    print("Add to Basket Response:", response.json())  # Должен вернуть сообщение об успехе

    # Тестирование API для добавления адреса доставки
    response = requests.post(base_url + 'user/contact', headers=headers, json={
        'city': 'New York',
        'street': '123 Main St',
        'phone': '123-456-7890'
    })
    print("Add Contact Response:", response.json())  # Должен вернуть сообщение об успехе

    # Тестирование API для подтверждения заказа
    response = requests.post(base_url + 'order', headers=headers, json={
        'contact': 1  
    })
    print("Order Confirmation Response:", response.json())  # Должен вернуть сообщение об успехе

    # Тестирование API для получения списка заказов
    response = requests.get(base_url + 'order', headers=headers)
    print("Orders List Response:", response.json())  # Должен вернуть список заказов

else:
    print("Failed to log in:", login_response.json())
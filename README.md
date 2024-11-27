# API Documentation

## Endpoints

### 1. User Registration

* **Method:** `POST`
* **URL:** `http://localhost:8000/api/v1/register/`
* **Description:** Register a new user in the system.
* **Parameters:**
	+ `first_name` (string) - User's first name.
	+ `last_name` (string) - User's last name.
	+ `email` (string) - User's email.
	+ `password` (string) - User's password.
* **Example Request:**
```bash
curl -X POST http://localhost:8000/api/v1/register/ -d "first_name=John&last_name=Doe&email=john.doe@example.com&password=secret"
```

### 2. User Authentication

* **Method:** `POST`
* **URL:** `http://localhost:8000/api/v1/login/`
* **Description:** Authenticate a user using email and password.
* **Parameters:**
	+ `email` (string) - User's email.
	+ `password` (string) - User's password.
* **Example Request:**
```bash
curl -X POST http://localhost:8000/api/v1/login/ -d "email=john.doe@example.com&password=secret"
```

### 3. Get Products List

* **Method:** `GET`
* **URL:** `http://localhost:8000/api/v1/products/`
* **Description:** Get a list of all available products.
* **Example Request:**
```bash
curl http://localhost:8000/api/v1/products/
```

### 4. Get Product Specification

* **Method:** `GET`
* **URL:** `http://localhost:8000/api/v1/products/{id}/`
* **Description:** Get information about a specific product by its ID.
* **Parameters:**
	+ `id` (integer) - Product ID.
* **Example Request:**
```bash
curl http://localhost:8000/api/v1/products/1/
```

### 5. Add Product to Cart

* **Method:** `POST`
* **URL:** `http://localhost:8000/api/v1/cart/`
* **Description:** Add a product to the cart.
* **Parameters:**
	+ `product_info_id` (integer) - Product ID.
	+ `quantity` (integer) - Product quantity.
* **Headers:**
	+ `Authorization: Token YOUR_TOKEN` - Authentication token.
* **Example Request:**
```bash
curl -X POST http://localhost:8000/api/v1/cart/ -d "product_info_id=1&quantity=2" -H "Authorization: Token YOUR_TOKEN"
```

### 6. Remove Product from Cart

* **Method:** `DELETE`
* **URL:** `http://localhost:8000/api/v1/cart/`
* **Description:** Remove a product from the cart.
* **Parameters:**
	+ `item_id` (integer) - Product ID in the cart.
* **Headers:**
	+ `Authorization: Token YOUR_TOKEN` - Authentication token.
* **Example Request:**
```bash
curl -X DELETE http://localhost:8000/api/v1/cart/ -d "item_id=1" -H "Authorization: Token YOUR_TOKEN"
```

### 7. Add Delivery Address

* **Method:** `POST`
* **URL:** `http://localhost:8000/api/v1/contacts/`
* **Description:** Add a new delivery address.
* **Parameters:**
	+ `first_name` (string) - Recipient's first name.
	+ `last_name` (string) - Recipient's last name.
	+ `email` (string) - Recipient's email.
	+ `phone` (string) - Recipient's phone number.
	+ `address` (string) - Street address.
	+ `city` (string) - City.
	+ `street` (string) - Street.
	+ `house` (string) - House number.
	+ `structure` (string) - Building number.
	+ `building` (string) - Apartment number.
* **Headers:**
	+ `Authorization: Token YOUR_TOKEN` - Authentication token.
    
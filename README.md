# E-Commerce API

A backend E-Commerce API built with **Django** and **Django REST Framework (DRF)**.

This project provides a complete RESTful backend for an online shopping platform, including user authentication, product and category management, shopping carts, checkout, orders, payments, reviews, wishlists, addresses, coupons, and notifications.

The project is designed with a modular Django application structure, role-based access control, JWT authentication, serializer validation, database relationships, and RESTful API endpoints.

## Project Overview

The E-Commerce API allows customers to browse products, manage their shopping cart, place orders, make payments using supported payment methods, review purchased products, and maintain a wishlist.

Administrators have additional privileges for managing products, categories, orders, payments, reviews, and other platform resources.

The application is built as an API-first backend, making it suitable for integration with web applications, mobile applications, or other frontend clients.

## Main Features

### Authentication and User Management

* Custom user authentication
* User registration
* User login
* JWT authentication
* Access and refresh tokens
* Authenticated API access
* Role-based access control
* Customer and administrator permissions
* User-specific resource filtering

### Product Management

* Product creation
* Product listing
* Product retrieval
* Product updating
* Product deletion
* Product pricing
* Product stock management
* Product availability
* Active/inactive products
* Category relationships
* Product filtering
* Product searching
* Product ordering

### Category Management

* Category creation
* Category listing
* Category retrieval
* Category updating
* Category deletion
* Product-category relationships
* Administrator-controlled category management

### Address Management

* Authenticated user addresses
* Create address
* List addresses
* Retrieve address
* Update address
* Delete address
* User-specific address filtering
* Address ownership validation

### Shopping Cart

* User-specific shopping carts
* Cart item management
* Add products to cart
* Update product quantities
* Remove products from cart
* Retrieve cart contents
* Product stock validation
* Authenticated cart access

### Checkout

The checkout process handles the complete transition from cart to order.

The checkout workflow includes:

1. Validate checkout information
2. Retrieve the authenticated user's cart
3. Check whether the cart exists
4. Check whether the cart contains items
5. Validate product availability
6. Validate product stock
7. Create the order
8. Create order items
9. Calculate the order total
10. Reduce product stock
11. Save the final order total
12. Clear the cart

Database transactions are used during checkout so that related operations are handled atomically.

### Orders

* Order creation
* Order retrieval
* User-specific order listing
* Administrator access to all orders
* Order total calculation
* Order item creation
* Order status management
* Order cancellation
* Stock restoration when eligible orders are cancelled

#### Order Statuses

Orders support the following statuses:

* Pending
* Confirmed
* Shipped
* Delivered
* Cancelled

Order status transitions are controlled to prevent invalid status changes.

For example:

```text
PENDING
   ├── CONFIRMED
   └── CANCELLED

CONFIRMED
   ├── SHIPPED
   └── CANCELLED

SHIPPED
   └── DELIVERED

DELIVERED
   └── Final state

CANCELLED
   └── Final state
```

### Order Items

Order items store the individual products belonging to an order.

Each order item contains information such as:

* Order
* Product
* Quantity
* Price

The product price is stored with the order item so that the order retains the price used when the order was created.

### Payments

The payment system is connected to orders using a one-to-one relationship.

Current payment functionality includes:

* Payment creation
* Payment retrieval
* Payment listing
* Payment status
* Payment amount
* Payment method
* Transaction identifier
* Payment timestamps
* User-specific payment access
* Administrator payment access

The current implementation supports:

```text
COD - Cash on Delivery
```

Payment statuses include:

* Pending
* Paid
* Failed
* Refunded

The payment amount should be determined by the backend from the associated order rather than trusting a customer-supplied amount.

### Product Reviews and Ratings

Customers can review products they have purchased.

Review functionality includes:

* Rating
* Comment
* Product relationship
* User relationship
* Order relationship
* Review timestamps
* Duplicate review prevention
* Order ownership validation
* Delivered-order validation
* Product/order validation
* Authenticated user assignment
* Administrator review deletion

Ratings are restricted to the valid rating range.

A customer cannot arbitrarily review a product. The backend verifies that the product belongs to an eligible order before allowing the review.

### Wishlist

Customers can maintain a personal wishlist.

Wishlist functionality includes:

* Wishlist creation
* Wishlist retrieval
* Wishlist updating
* Wishlist deletion
* User-specific wishlist access
* Administrator access
* Wishlist item management

### Wishlist Items

Wishlist items connect products to a user's wishlist.

Features include:

* Add product to wishlist
* Retrieve wishlist items
* Update wishlist items
* Remove wishlist items
* Wishlist ownership validation
* Duplicate product prevention
* User-specific filtering
* Administrator access

The API prevents a customer from adding products to another user's wishlist.

A product cannot be added multiple times to the same wishlist.

### Coupons

The project contains a dedicated coupons application for implementing discount-related functionality.

The coupon system is designed to support e-commerce discount management and can be extended with additional business rules such as:

* Coupon codes
* Discount values
* Expiration dates
* Usage limits
* Minimum order amounts
* Active/inactive coupons

### Notifications

The project contains a dedicated notifications application for handling user-facing notification functionality.

This provides a foundation for notifying customers about events such as:

* Order confirmation
* Order status changes
* Shipping updates
* Delivery
* Payment updates
* Other e-commerce events

## Technology Stack

### Backend

* Python
* Django
* Django REST Framework

### Authentication

* JWT Authentication
* REST Framework Simple JWT

### Database

The project uses Django's ORM and can be configured with a supported relational database.

SQLite can be used for local development, while PostgreSQL or another production-ready relational database can be configured for deployment.

### API Documentation

The project can be integrated with API documentation tools such as:

* Swagger UI
* OpenAPI
* DRF Spectacular

## Project Structure

The repository follows a modular Django structure.

```text
E_Commerce/
│
├── apps/
│   │
│   ├── accounts/
│   ├── addresses/
│   ├── cart/
│   ├── cartitem/
│   ├── categories/
│   ├── coupons/
│   ├── notifications/
│   ├── orderItems/
│   ├── orders/
│   ├── payments/
│   ├── products/
│   ├── reviews/
│   └── wishlist/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirement.txt
├── .gitignore
└── README.md
```

The repository currently contains these application modules under `apps/`.

## Application Responsibilities

| App             | Responsibility                               |
| --------------- | -------------------------------------------- |
| `accounts`      | Users, authentication, roles and permissions |
| `addresses`     | Customer shipping addresses                  |
| `products`      | Product management and stock                 |
| `categories`    | Product categories                           |
| `cart`          | Shopping cart                                |
| `cartitem`      | Products and quantities inside carts         |
| `orders`        | Order creation, checkout and order status    |
| `orderItems`    | Products belonging to orders                 |
| `payments`      | Order payment records                        |
| `reviews`       | Product reviews and ratings                  |
| `wishlist`      | Customer wishlists and wishlist items        |
| `coupons`       | Discount and coupon functionality            |
| `notifications` | Customer notification functionality          |

## Authentication

The API uses JWT-based authentication.

After authentication, the client receives an access token and a refresh token.

Authenticated requests should include:

```http
Authorization: Bearer <access_token>
```

Protected endpoints require a valid authentication token.

## User Roles

The application uses role-based authorization.

### Customer

Customers can:

* Manage their profile
* Manage their addresses
* Browse products
* Manage their cart
* Checkout
* Create orders
* View their orders
* Cancel eligible orders
* View their payments
* Review eligible products
* Manage their wishlist

### Administrator

Administrators have broader access and can:

* Manage products
* Manage categories
* View all orders
* Update order status
* View payments
* Manage reviews
* Access all wishlists
* Access administrative resources

## API Design

The application follows RESTful API principles using Django REST Framework `ModelViewSet`.

Standard operations include:

```text
GET     /resource/
POST    /resource/
GET     /resource/{id}/
PUT     /resource/{id}/
PATCH   /resource/{id}/
DELETE  /resource/{id}/
```

Custom business operations use DRF `@action` endpoints.

Examples include:

```text
POST /orders/checkout/
PATCH /orders/{id}/update_status/
POST /orders/{id}/cancel/
```

## Data Ownership

User-specific data is protected at the queryset level.

For example, customers should only receive records belonging to their authenticated account.

This approach prevents users from simply changing an object ID and accessing another user's resources.

Examples of user-specific resources include:

* Addresses
* Cart
* Orders
* Payments
* Reviews
* Wishlists
* Wishlist items

Administrators can be granted broader access where required.

## Validation

Validation is implemented at multiple levels.

### Serializer Validation

Serializers validate incoming API data before database operations.

Examples include:

* Address ownership
* Wishlist ownership
* Duplicate wishlist products
* Review eligibility
* Review order ownership
* Product/order relationships
* Rating values

### Database Constraints

Database-level constraints are also used where appropriate.

For example, wishlist items can prevent duplicate product entries through unique constraints.

### Business Logic Validation

Complex business rules are handled in ViewSets and service logic.

Examples include:

* Stock validation
* Checkout validation
* Order status transitions
* Order cancellation rules
* Stock restoration
* Payment-related validation

## Checkout Flow

The checkout process follows this flow:

```text
Customer
   |
   v
Shopping Cart
   |
   v
Validate Cart
   |
   v
Validate Products
   |
   v
Validate Stock
   |
   v
Create Order
   |
   v
Create Order Items
   |
   v
Calculate Total
   |
   v
Reduce Stock
   |
   v
Clear Cart
   |
   v
Order Created
```

The checkout operation is wrapped in a database transaction so related database changes can be rolled back if an operation fails.

## Order Cancellation Flow

Eligible orders can be cancelled by the customer or administrator according to the application's permission rules.

When an eligible order is cancelled:

```text
Order
   |
   v
Get Order Items
   |
   v
Restore Product Stock
   |
   v
Set Order Status = CANCELLED
```

This ensures stock is returned to inventory when a cancellable order is cancelled.

## Reviews Flow

A customer review follows validation rules before creation:

```text
Authenticated User
        |
        v
Check Order Ownership
        |
        v
Check Order Status
        |
        v
Check Product Belongs to Order
        |
        v
Check Duplicate Review
        |
        v
Validate Rating
        |
        v
Create Review
```

This prevents users from reviewing products they did not purchase through an eligible order.

## Wishlist Flow

Wishlist management follows:

```text
Authenticated User
        |
        v
Get Own Wishlist
        |
        v
Select Product
        |
        v
Check Wishlist Ownership
        |
        v
Check Duplicate Product
        |
        v
Create Wishlist Item
```

This prevents unauthorized wishlist access and duplicate products within the same wishlist.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/waqaralisoomro915-cloud/E_Commerce.git
```

### 2. Move into the project directory

```bash
cd E_Commerce
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Linux/macOS:

```bash
python3 -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 5. Install dependencies

The repository includes a `requirement.txt` dependency file.

Run:

```bash
pip install -r requirement.txt
```

### 6. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create the administrator account.

### 8. Run the development server

```bash
python manage.py runserver
```

The API will normally be available at:

```text
http://127.0.0.1:8000/
```

## Environment Variables

For production, sensitive configuration should be stored in environment variables rather than committed to Git.

Typical environment variables may include:

```env
SECRET_KEY=your-secret-key
DEBUG=False

DB_NAME=your_database
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

Do not commit real passwords, secret keys, API keys, or other sensitive credentials.

## Database Migrations

Whenever models are changed:

```bash
python manage.py makemigrations
python manage.py migrate
```

To inspect migration status:

```bash
python manage.py showmigrations
```

## Running Tests

If tests are added to the project, they can be executed with:

```bash
python manage.py test
```

For a specific application:

```bash
python manage.py test apps.accounts
```

## API Documentation

When OpenAPI/Swagger documentation is configured, API endpoints can be explored interactively through the generated documentation interface.

This is useful for:

* Testing endpoints
* Viewing request parameters
* Inspecting serializers
* Testing authentication
* Understanding response structures

## Security Considerations

The API uses authentication and authorization to protect user-specific resources.

Important security practices include:

* JWT authentication
* Authenticated access to protected endpoints
* Role-based permissions
* User-specific querysets
* Serializer-level validation
* Database-level constraints
* Ownership checks
* Backend-controlled order totals
* Backend-controlled stock updates
* Transactional checkout processing

The backend should never trust sensitive values supplied directly by the customer.

For example, the final order amount should be calculated from trusted product prices and quantities rather than accepting an arbitrary amount from the client.

## Future Improvements

Possible future improvements include:

* Stripe or other online payment gateway integration
* Payment webhook handling
* Email notifications
* Order confirmation emails
* Password reset email workflow
* Product image management
* Advanced coupon rules
* Discount calculation during checkout
* Shipping fee calculation
* Tax calculation
* Product variants
* Inventory management
* Advanced product filtering
* Product recommendations
* Search optimization
* Redis caching
* Background tasks with Celery
* Rate limiting improvements
* Automated API tests
* Docker support
* CI/CD pipeline
* Production deployment configuration

## Development Goals

This project is being developed as a practical backend engineering project to strengthen skills in:

* Django
* Django REST Framework
* REST API development
* Database relationships
* Authentication
* Authorization
* Serializer validation
* Queryset filtering
* Transactions
* E-commerce business logic
* API architecture
* Git and GitHub

## Git Workflow

The project uses Git for version control.

Typical workflow:

```bash
git status
git add -A
git commit -m "feat: describe your feature"
git push origin main
```

Feature-oriented commit messages follow a conventional style such as:

```text
feat: add product management
feat: implement checkout
feat: add order cancellation
feat: add product reviews and ratings
feat: add wishlist and wishlist item management
```

## Project Status

The project currently contains the core e-commerce backend modules including:

* Accounts
* Addresses
* Products
* Categories
* Cart
* Cart Items
* Orders
* Order Items
* Payments
* Reviews
* Wishlist
* Wishlist Items
* Coupons
* Notifications

The repository currently contains 13 commits and is publicly available on GitHub.

## Repository

GitHub:

https://github.com/waqaralisoomro915-cloud/E_Commerce

## Author

**Waqar Ali**

Software Engineering Student
Backend / Django Developer

## License

This project is currently intended for educational and portfolio purposes.

If you plan to distribute or reuse the project publicly, add an appropriate open-source license such as the MIT License.

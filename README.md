# Ecommerce Django Project

A full-featured ecommerce web application built with Django, featuring product management, shopping cart, payment integration, and user accounts.

## Features

### Core Features
- **Product Management**: Categories, products with size and color variants
- **Shopping Cart**: Add to cart, update quantities, remove items
- **Coupon System**: Apply discount coupons with minimum order requirements
- **Payment Integration**: Razorpay payment gateway integration
- **Invoice Generation**: Automatic PDF invoice generation after payment
- **Email Notifications**: Invoice emails with PDF attachments
- **User Authentication**: Registration, login, email verification
- **User Profiles**: Complete profile management with address details
- **Search Functionality**: Search products by name and description
- **Category Browsing**: Browse products by category

### Technical Features
- Session-based cart for anonymous users
- User-based cart for authenticated users
- Dynamic price calculation based on size and color variants
- Image management with color-specific product images
- Responsive design with Bootstrap 4
- Admin panel for managing all entities

## Project Structure

```
Ecommerce/
├── accounts/          # User authentication and profiles
├── base/             # Base models and email utilities
├── cart/             # Shopping cart and payment functionality
├── home/             # Homepage and search
├── products/         # Product, category, and variant models
├── templates/        # HTML templates
├── public/static/    # Static files (CSS, JS, images)
└── Ecommerce/        # Project settings and URLs
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip
- Virtual environment (recommended)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd Ecommerce
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv myenv
   # On Windows
   myenv\Scripts\activate
   # On Linux/Mac
   source myenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure settings**
   - Open `Ecommerce/settings.py`
   - Update Razorpay keys:
     ```python
     RAZORPAY_KEY_ID = 'your_razorpay_key_id'
     RAZORPAY_KEY_SECRET = 'your_razorpay_secret_key'
     ```
   - Configure email settings (already configured for Gmail)

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Populate database with sample data**
   ```bash
   python manage.py populate_db
   ```
   Note: This creates categories, products, variants, and coupons. Images need to be added manually.

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Website: http://127.0.0.1:8000
   - Admin Panel: http://127.0.0.1:8000/admin

## Database Population

The project includes a management command to populate the database with sample data:

```bash
python manage.py populate_db
```

This command creates:
- 8 Categories (Electronics, Clothing, Home & Living, Books, Sports, Beauty, Toys, Automotive)
- 6 Size Variants (XS, S, M, L, XL, XXL)
- 10 Color Variants (Red, Blue, Green, Black, White, Yellow, Pink, Purple, Orange, Grey)
- 40+ Products across all categories
- 6 Coupons (including expired ones)

**Note**: Images are not included. You need to add product and category images through the admin panel.

## Models

### Products App
- **Category**: Product categories with images
- **Product**: Main product model with name, price, description
- **SizeVariant**: Size options with price adjustments
- **ColorVariant**: Color options with price adjustments
- **ProductImage**: Product images linked to color variants

### Cart App
- **Cart**: User shopping cart
- **CartItems**: Individual items in cart with variants
- **Coupon**: Discount coupons with validation
- **Payment**: Payment records with Razorpay integration

### Accounts App
- **Profile**: Extended user profile with address and personal info

## Admin Panel

Access the admin panel at `/admin` to manage:
- Categories and Products
- Size and Color Variants
- Product Images
- Coupons
- Carts and Cart Items
- Payments
- User Profiles

## API Endpoints / URLs

### Home & Products
- `/` - Homepage with products
- `/search/?q=query` - Search products
- `/product/<slug>/` - Product detail page
- `/product/category/<slug>/` - Category products page

### Authentication
- `/accounts/login/` - User login
- `/accounts/register/` - User registration
- `/accounts/logout/` - User logout
- `/accounts/account/` - User account/profile page
- `/accounts/activate/<token>/` - Email activation

### Cart
- `/cart/` - View cart
- `/cart/add/` - Add to cart (POST)
- `/cart/update/<item_id>/` - Update cart item (POST)
- `/cart/remove/<item_id>/` - Remove from cart (POST)
- `/cart/coupon/apply/` - Apply coupon (POST)
- `/cart/coupon/remove/` - Remove coupon (POST)
- `/cart/payment/` - Initiate payment
- `/cart/payment/verify/` - Verify payment (POST)
- `/cart/payment/success/<payment_id>/` - Payment success page

## Payment Integration

### Razorpay Setup
1. Sign up at [Razorpay](https://razorpay.com/)
2. Get your API keys from Dashboard > Settings > API Keys
3. Update `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` in settings.py
4. Use test mode for development

### Test Cards
- Success: 4111 1111 1111 1111
- Failure: 4000 0000 0000 0002
- CVV: Any 3 digits
- Expiry: Any future date

## Email Configuration

The project uses Gmail SMTP. Update these in `settings.py`:
- `EMAIL_HOST_USER`: Your Gmail address
- `EMAIL_HOST_PASSWORD`: Gmail app password

To generate app password:
1. Enable 2-factor authentication
2. Go to Google Account > Security > App passwords
3. Generate password for "Mail"

## Environment Variables (Optional)

For production, consider using environment variables:
```python
import os

RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

## Static Files

Static files are served from `public/static/`. In production:
1. Run `python manage.py collectstatic`
2. Configure web server to serve static files

## Media Files

Media files (uploads) are stored in `public/static/`. Ensure:
- `public/static/categories/` - Category images
- `public/static/product/` - Product images
- `public/static/profile/` - Profile images
- `public/static/invoices/` - Generated invoices

## Testing

### Manual Testing Checklist
- [ ] User registration and email verification
- [ ] User login and logout
- [ ] Product browsing and search
- [ ] Add products to cart
- [ ] Update cart quantities
- [ ] Apply and remove coupons
- [ ] Payment flow with Razorpay
- [ ] Invoice generation and email
- [ ] Profile management
- [ ] Category filtering

## Troubleshooting

### Common Issues

1. **Migration errors**
   - Delete `db.sqlite3` and migration files (except `__init__.py`)
   - Run `python manage.py makemigrations` and `migrate`

2. **Razorpay payment not working**
   - Verify API keys in settings
   - Check Razorpay dashboard for logs
   - Ensure using test keys in development

3. **Email not sending**
   - Verify Gmail credentials
   - Check app password is correct
   - Ensure less secure apps access (if not using app password)

4. **Images not displaying**
   - Check MEDIA_URL and MEDIA_ROOT in settings
   - Verify file paths in templates
   - Ensure images are uploaded to correct directories

## Development

### Adding New Features
1. Create models in appropriate app
2. Run migrations
3. Create views and URLs
4. Create templates
5. Update admin if needed

### Code Structure
- Models: Define in `models.py`
- Views: Business logic in `views.py`
- Templates: HTML in `templates/` directory
- URLs: Route definitions in `urls.py`
- Admin: Configuration in `admin.py`

## Production Deployment

### Checklist
- [ ] Set `DEBUG = False` in settings
- [ ] Update `ALLOWED_HOSTS`
- [ ] Use environment variables for secrets
- [ ] Configure proper database (PostgreSQL recommended)
- [ ] Set up static file serving
- [ ] Configure HTTPS
- [ ] Set up proper email service
- [ ] Use production Razorpay keys
- [ ] Set up backup strategy
- [ ] Configure logging

## Technologies Used

- **Backend**: Django 5.2.8
- **Database**: SQLite (development), PostgreSQL (production recommended)
- **Frontend**: Bootstrap 4, jQuery
- **Payment**: Razorpay
- **PDF Generation**: ReportLab
- **Email**: Django Email Backend

## License

This project is open source and available for educational purposes.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Django and Razorpay documentation
3. Check admin panel for data issues

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Author

Developed as a comprehensive ecommerce solution with modern features and best practices.

---

**Note**: Remember to add product and category images through the admin panel after running `populate_db`. The script creates all data except images.


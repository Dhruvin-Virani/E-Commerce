"""
Management command to populate the database with sample data
Run: python manage.py populate_db
"""

from django.core.management.base import BaseCommand
from products.models import Category, Product, SizeVariant, ColorVariant, ProductImage
from cart.models import Coupon
import random


class Command(BaseCommand):
    help = 'Populates the database with sample data (excluding images)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))
        
        # Create Categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'description': 'Fashion and apparel'},
            {'name': 'Home & Living', 'description': 'Home decor and furniture'},
            {'name': 'Books', 'description': 'Books and literature'},
            {'name': 'Sports', 'description': 'Sports and fitness equipment'},
            {'name': 'Beauty', 'description': 'Beauty and personal care'},
            {'name': 'Toys', 'description': 'Toys and games'},
            {'name': 'Automotive', 'description': 'Car accessories and parts'},
        ]
        
        categories = []
        for cat_data in categories_data:
            # Check if category exists
            try:
                category = Category.objects.get(category_name=cat_data['name'])
                created = False
            except Category.DoesNotExist:
                # Create category without image (will need to be added manually)
                category = Category.objects.create(
                    category_name=cat_data['name']
                )
                # Note: category_image will need to be added through admin
                created = True
            
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.category_name}'))
        
        # Create Size Variants
        sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
        size_variants = []
        for size in sizes:
            size_obj, created = SizeVariant.objects.get_or_create(
                size=size,
                defaults={'price': random.randint(0, 500)}
            )
            size_variants.append(size_obj)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created size variant: {size}'))
        
        # Create Color Variants
        colors_data = [
            {'name': 'Red', 'price': 0},
            {'name': 'Blue', 'price': 0},
            {'name': 'Green', 'price': 0},
            {'name': 'Black', 'price': 100},
            {'name': 'White', 'price': 0},
            {'name': 'Yellow', 'price': 0},
            {'name': 'Pink', 'price': 50},
            {'name': 'Purple', 'price': 50},
            {'name': 'Orange', 'price': 0},
            {'name': 'Grey', 'price': 0},
        ]
        
        color_variants = []
        for color_data in colors_data:
            color_obj, created = ColorVariant.objects.get_or_create(
                color_name=color_data['name'],
                defaults={'price': color_data['price']}
            )
            color_variants.append(color_obj)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created color variant: {color_obj.color_name}'))
        
        # Create Products
        products_data = [
            # Electronics
            {'name': 'Smartphone Pro Max', 'category': 'Electronics', 'price': 45000, 'description': 'Latest smartphone with advanced features, high-resolution camera, and long battery life.'},
            {'name': 'Wireless Headphones', 'category': 'Electronics', 'price': 3500, 'description': 'Premium wireless headphones with noise cancellation and 30-hour battery.'},
            {'name': 'Laptop Ultra', 'category': 'Electronics', 'price': 75000, 'description': 'High-performance laptop perfect for work and gaming.'},
            {'name': 'Smart Watch', 'category': 'Electronics', 'price': 12000, 'description': 'Feature-rich smartwatch with health tracking and notifications.'},
            {'name': 'Tablet Pro', 'category': 'Electronics', 'price': 25000, 'description': 'Versatile tablet for work and entertainment.'},
            
            # Clothing
            {'name': 'Cotton T-Shirt', 'category': 'Clothing', 'price': 599, 'description': 'Comfortable cotton t-shirt available in multiple colors and sizes.'},
            {'name': 'Denim Jeans', 'category': 'Clothing', 'price': 1999, 'description': 'Classic fit denim jeans with stretch comfort.'},
            {'name': 'Formal Shirt', 'category': 'Clothing', 'price': 1299, 'description': 'Premium formal shirt for office wear.'},
            {'name': 'Running Shoes', 'category': 'Clothing', 'price': 3499, 'description': 'Comfortable running shoes with cushioned sole.'},
            {'name': 'Winter Jacket', 'category': 'Clothing', 'price': 4999, 'description': 'Warm winter jacket with water-resistant material.'},
            
            # Home & Living
            {'name': 'Coffee Table', 'category': 'Home & Living', 'price': 8999, 'description': 'Modern coffee table with storage space.'},
            {'name': 'Bed Sheets Set', 'category': 'Home & Living', 'price': 1299, 'description': 'Soft cotton bed sheets set with pillow covers.'},
            {'name': 'Wall Clock', 'category': 'Home & Living', 'price': 899, 'description': 'Elegant wall clock for home decor.'},
            {'name': 'Dining Table Set', 'category': 'Home & Living', 'price': 25000, 'description': 'Complete dining table set for 6 people.'},
            {'name': 'LED Lamp', 'category': 'Home & Living', 'price': 599, 'description': 'Energy-efficient LED table lamp.'},
            
            # Books
            {'name': 'Python Programming Guide', 'category': 'Books', 'price': 599, 'description': 'Comprehensive guide to Python programming.'},
            {'name': 'Web Development Handbook', 'category': 'Books', 'price': 799, 'description': 'Complete handbook for web development.'},
            {'name': 'Data Science Essentials', 'category': 'Books', 'price': 999, 'description': 'Essential concepts of data science.'},
            {'name': 'Fiction Novel Collection', 'category': 'Books', 'price': 499, 'description': 'Bestselling fiction novel collection.'},
            {'name': 'Business Strategy Book', 'category': 'Books', 'price': 699, 'description': 'Learn business strategies from experts.'},
            
            # Sports
            {'name': 'Yoga Mat', 'category': 'Sports', 'price': 799, 'description': 'Non-slip yoga mat for exercise.'},
            {'name': 'Dumbbell Set', 'category': 'Sports', 'price': 2999, 'description': 'Adjustable dumbbell set for home gym.'},
            {'name': 'Football', 'category': 'Sports', 'price': 599, 'description': 'Professional quality football.'},
            {'name': 'Tennis Racket', 'category': 'Sports', 'price': 3499, 'description': 'Lightweight tennis racket for professionals.'},
            {'name': 'Basketball', 'category': 'Sports', 'price': 899, 'description': 'Official size basketball.'},
            
            # Beauty
            {'name': 'Face Cream', 'category': 'Beauty', 'price': 499, 'description': 'Moisturizing face cream for all skin types.'},
            {'name': 'Lipstick Set', 'category': 'Beauty', 'price': 799, 'description': 'Set of 6 long-lasting lipsticks.'},
            {'name': 'Perfume', 'category': 'Beauty', 'price': 1299, 'description': 'Premium fragrance for men and women.'},
            {'name': 'Hair Shampoo', 'category': 'Beauty', 'price': 299, 'description': 'Nourishing shampoo for healthy hair.'},
            {'name': 'Sunscreen Lotion', 'category': 'Beauty', 'price': 399, 'description': 'SPF 50+ sunscreen for protection.'},
            
            # Toys
            {'name': 'Action Figure Set', 'category': 'Toys', 'price': 999, 'description': 'Collectible action figure set.'},
            {'name': 'Board Game', 'category': 'Toys', 'price': 599, 'description': 'Family board game for all ages.'},
            {'name': 'Remote Control Car', 'category': 'Toys', 'price': 1499, 'description': 'High-speed remote control car.'},
            {'name': 'Building Blocks', 'category': 'Toys', 'price': 799, 'description': 'Educational building blocks set.'},
            {'name': 'Puzzle Set', 'category': 'Toys', 'price': 499, 'description': '1000-piece jigsaw puzzle.'},
            
            # Automotive
            {'name': 'Car Phone Mount', 'category': 'Automotive', 'price': 399, 'description': 'Universal car phone mount holder.'},
            {'name': 'Car Charger', 'category': 'Automotive', 'price': 299, 'description': 'Fast charging car charger.'},
            {'name': 'Car Seat Cover', 'category': 'Automotive', 'price': 1999, 'description': 'Premium car seat covers set.'},
            {'name': 'Car Air Freshener', 'category': 'Automotive', 'price': 199, 'description': 'Long-lasting car air freshener.'},
            {'name': 'Car Floor Mat', 'category': 'Automotive', 'price': 1499, 'description': 'Waterproof car floor mats.'},
        ]
        
        created_products = 0
        for prod_data in products_data:
            category = next((c for c in categories if c.category_name == prod_data['category']), None)
            if not category:
                continue
            
            product, created = Product.objects.get_or_create(
                product_name=prod_data['name'],
                defaults={
                    'category': category,
                    'price': prod_data['price'],
                    'product_description': prod_data['description']
                }
            )
            
            if created:
                created_products += 1
                # Add random size variants (for clothing and some products)
                if category.category_name == 'Clothing' or random.choice([True, False]):
                    product.size_variant.add(*random.sample(size_variants, random.randint(2, 4)))
                
                # Add random color variants
                product.color_variant.add(*random.sample(color_variants, random.randint(2, 5)))
                
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.product_name}'))
        
        # Create Coupons
        coupons_data = [
            {'code': 'WELCOME10', 'discount': 100, 'minimum': 500, 'expired': False},
            {'code': 'SAVE20', 'discount': 200, 'minimum': 1000, 'expired': False},
            {'code': 'BIG50', 'discount': 500, 'minimum': 5000, 'expired': False},
            {'code': 'FLAT100', 'discount': 100, 'minimum': 1000, 'expired': False},
            {'code': 'NEWUSER', 'discount': 150, 'minimum': 800, 'expired': False},
            {'code': 'EXPIRED', 'discount': 200, 'minimum': 1000, 'expired': True},
        ]
        
        for coupon_data in coupons_data:
            coupon, created = Coupon.objects.get_or_create(
                coupon_code=coupon_data['code'],
                defaults={
                    'discount_price': coupon_data['discount'],
                    'minimum_amount': coupon_data['minimum'],
                    'is_expired': coupon_data['expired']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created coupon: {coupon.coupon_code}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nDatabase population completed!'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} categories'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(size_variants)} size variants'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(color_variants)} color variants'))
        self.stdout.write(self.style.SUCCESS(f'Created {created_products} products'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(coupons_data)} coupons'))
        self.stdout.write(self.style.WARNING('\nNote: Images need to be added manually through admin panel or by uploading files.'))


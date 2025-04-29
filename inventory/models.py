import uuid

from django.db import models

class Brand(models.Model):
    """
    Brand model represents a brand of a product. 
    E.g., Nike, Adidas, Samsung, Apple, etc.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    """
    Category model represents a category of a product. 
    E.g., Gloceries, Fashion, Clothing, Shoes, Clothes, Electronics, Phones, etc.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product model represents a product.
    E.g Samsung Galaxy S21, Apple iPhone 13, etc.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/')
    brand = models.OneToOneField(Brand, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class ProductGallery(models.Model):
    """
    ProductGallery model represents a gallery of images or videos for a product.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery')
    media = models.FileField(upload_to='gallery/products/')
    uploaded_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Gallery for {self.product.name}"


class ProductSpecification(models.Model):
    """
    ProductSpecification model represents a specification of a product.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}: {self.value}"
    
    
class ProductAttributeType(models.Model):
    """
    ProductAttributeType model represents a type of attribute for a product.
    E.g., Color, Size, Material, etc.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    

class ProductAttributeOption(models.Model):
    """
    ProductAttributeOption model represents an option of an attribute for a product.
    E.g for Color, Red, Blue, Green, etc.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    attribute_type = models.ForeignKey(ProductAttributeType, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.attribute_type.name} - {self.name}'
    
    
class ProductVariant(models.Model):
    """
    ProductVariant model represents a variant of a product.
    E.g., Red Shirt, 128 GB, etc.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.name} - {self.sku}"
    
    
class ProductVariantAttribute(models.Model):
    """
    ProductVariantAttribute model represents an attribute of a variant of a product.
    This connects a variant with an attribute.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='attributes')
    attribute_option = models.ForeignKey(ProductAttributeOption, on_delete=models.CASCADE, related_name='variants')

    def __str__(self):
        return f"{self.variant} - {self.attribute_option.name}"

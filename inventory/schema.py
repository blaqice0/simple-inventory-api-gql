import graphene

from graphene_django import DjangoObjectType

from .models import (
    Brand,
    Category,
    Product,
)

class BrandType(DjangoObjectType):
    class Meta:
        model = Brand
        exclude = ('id',)
    

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        exclude = ('id',)
        

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        exclude = ('id',)


class Query(graphene.ObjectType):
    brands = graphene.List(BrandType)
    categories = graphene.List(CategoryType)
    products = graphene.List(ProductType)

    def resolve_brands(root, info, **kwargs):
        return Brand.objects.all()
    
    def resolve_categories(root, info, **kwargs):
        return Category.objects.all()

    def resolve_products(root, info, **kwargs):
        return Product.objects.select_related('category', 'brand').all()
    
    
schema = graphene.Schema(query=Query)

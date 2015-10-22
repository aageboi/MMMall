from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    picture = models.ImageField(upload_to='pictures/', default='pictures/noimage.png')
    price = models.DecimalField(decimal_places=2, max_digits=24, default=0)
    brand = models.ForeignKey(Brand)
    category = models.ForeignKey('Category')
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return "%s (%s)" % (self.title, self.brand.name)


class Category(models.Model):
    name = models.CharField(max_length=128)
    parent = models.ForeignKey("self", related_name="children", blank=True, null=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User)
    total = models.DecimalField(decimal_places=2, max_digits=24, default=0)
    checked_out = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s at %s" % (self.user.get_full_name(), self.total)


class CartItem(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart)

    def __str__(self):
        return "%s x%s" % (self.product.title, self.quantity)
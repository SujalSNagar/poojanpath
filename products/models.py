from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.CharField(max_length=240, blank=True)

    image = models.ImageField(upload_to='categories/',blank=True,null=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category', args=[self.slug])


class SubCategory(models.Model):

    category = models.ForeignKey(
        Category,
        related_name='subcategories',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=120)

    slug = models.SlugField(max_length=140)

    class Meta:
        ordering = ['name']

        unique_together = ['category', 'slug']

        verbose_name_plural = 'subcategories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    subcategory = models.ForeignKey(
    SubCategory,
    related_name='products',
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=False, null=False)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.slug])


class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to='products/gallery/'
    )

    alt_text = models.CharField(
        max_length=120,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.product.name
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Accessory(models.Model):
    CATEGORY_CHOICES = [
        ('charger', 'Charger'),
        ('bag', 'Bag'),
        ('mouse', 'Mouse'),
        ('keyboard', 'Keyboard'),
        ('adapter', 'Adapter'),
        ('stand', 'Stand'),
        ('laptop', 'Laptop'),
        ('printer', 'Printer'),
        ('memory', 'Memory'),
        ('spiker', 'Spiker'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='accessory_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    query = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

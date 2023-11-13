from django.db import models
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    category_description = models.CharField(max_length=255, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.category_description}"
    
class Sub_Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    sub_Category_description = models.CharField(max_length=255, null=True, blank=True)
    main_category = models.OneToOneField(Category,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.main_category}, {self.name}"
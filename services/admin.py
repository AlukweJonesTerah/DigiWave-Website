from django.contrib import admin
from .models import Category, Sub_Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_description')
    prepopulated_fields = {'slug': ("name", "category_description")}

admin.site.register(Category, CategoryAdmin)

class Sub_Category_Admin(admin.ModelAdmin):
    list_display = ('main_category', 'name', 'sub_Category_description')
    prepopulated_fields = {'slug': ("main_category", "name", "sub_Category_description")}

admin.site.register(Sub_Category, Sub_Category_Admin)

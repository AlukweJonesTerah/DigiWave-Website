from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.categories, name='categories_list'),
    path('categories/add_category', views.adding_category, name='add_category'),
    path('categories/details/<slug:slug>/', views.category_detail, name='category_detail'),
    path('categories/update/<slug:slug>/', views.update_category, name='update_category'),
    path('categories/delete/<slug:slug>/', views.delete_category, name='delete_category'),
    path('categories/delete_all/', views.delete_all_categories, name='delete_all_categories'),
    
    path('categories/sub_category/<slug:slug>/', views.adding_sub_category, name='add_sub_category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
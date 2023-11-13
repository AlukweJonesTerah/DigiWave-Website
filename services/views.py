from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q
from .forms import CategoryForm, CategoryUpdateForm, DeleteAllCategoriesForm, CategoryDeleteForm, Sub_CategoryForm
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseRedirect
from django.template import  loader
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from .models import Category, Sub_Category
from django.contrib import messages


def adding_category(request):
    template = 'category_add.html'
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        try:
            if form.is_valid():
                new_category = form.save()
                messages.success(request, 'Category added successfully!')
                return redirect('services:category_detail', slug=new_category.slug)
        except IntegrityError:
            messages.error(request, 'This slug is already in use. Please choose a different one.')
        except ValidationError as e:
                messages.error(request, f'Validation error: {str(e)}')
        except AttributeError as e:
                messages.error(request, f'Attribute error: {str(e)}')
        except Exception as e:
                messages.error(request, f'Error adding a category: {str(e)}')

    else:
        form = CategoryForm()

    context = {'form': form}
    return render(request, template, context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    context = {'category': category}
    return render(request, 'category_detail.html', context)

def categories(request):
    categories_list = Category.objects.all()
    context = {'categories': categories_list}
    return render(request, 'category_list.html', context)

def update_category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    if request.method == 'POST':
        form = CategoryUpdateForm(request.POST, request.FILES, instance=category)
        try:
            if form.is_valid():
                try:
                    new_slug = form.cleaned_data['slug']
                    if new_slug != slug:
                        # User has changed the slug, check if it is unique
                        if  Category.objects.filter(slug=new_slug).exists():
                            messages.error(request, 'Slug must be unique. Please choose a different one.')
                            context={
                                'form': form,
                                'category': category
                            }
                            return render(request, 'category_update.html', context)
                        category.slug = new_slug #Update the slug                            
                    form.save()
                    messages.success(request, 'Category updated successfully!')
                    return redirect('services:category_detail', slug=slug)
                except Exception as e:
                    messages.error(request, f'Error updatig category: {str(e)}')
            else:
                messages.error(request, 'Form fields were invalid!')
                return render(request, 'category_update.html', {'form': form, 'category': category})
        except IntegrityError as e:
            messages.error(request, f'Integrity Error: {str(e)}')
        except ValidationError as e:
            messages.error(request, f'Validation error: {str(e)}')
        except AttributeError as e:
            messages.error(request, f'Attribute error: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error updating category: {str(e)}')            
    else:
        form = CategoryUpdateForm(instance=category)

    return render(request, 'category_update.html', {'form': form, 'category': category})


def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    confirm_form = CategoryDeleteForm()

    if request.method == 'POST':
        # Check if the confirmation form is submitted
        confirm_form = CategoryDeleteForm(request.POST)
        if confirm_form.is_valid() and confirm_form.cleaned_data.get('confirm_delete'):
            # Optionally, you can check for other conditions before deletion
            try:
                if category:
                    category.delete()
                    messages.success(request, 'Category deleted successfully')
                else:
                    messages.error(request, "No category to delete!")
            except IntegrityError:
                messages.error(request, f'Integrity Error: {str(e)}')
            except ValidationError as e:
                messages.error(request, f'Validation error: {str(e)}')
            except AttributeError as e:
                messages.error(request, f'Attribute error: {str(e)}')
            except Exception as e:
                messages.error(request, f'Error deleting category: {str(e)}')
            else:
                return redirect('services:categories_list')  # Redirect to the list of categories or another relevant page after deletion
        else:
            messages.error(request, 'Form validation failed.')

    context = {'category': category, 'confirm_form': confirm_form}
    return render(request, 'delete_category.html', context)



def delete_all_categories(request):
    if request.method == 'POST':
        confirm_form = DeleteAllCategoriesForm(request.POST)
        if confirm_form.is_valid() and confirm_form.cleaned_data.get('confirm_delete_all'):
            categories = Category.objects.all()
            try:
                if categories.exists():
                    # Delete each category
                    for category in categories:
                        category.delete()

                    messages.success(request, 'All categories deleted successfully!')
                    return redirect('services:categories_list')
                else:
                    messages.error(request, "No categories to delete!")
            except IntegrityError:
                messages.error(request, 'This slug is already in use. Please choose a different one.')
            except ValidationError as e:
                messages.error(request, f'Validation error: {str(e)}')
            except AttributeError as e:
                messages.error(request, f'Attribute error: {str(e)}')
            except Exception as e:
                messages.error(request, f'Error deleting categories: {str(e)}')   
        else:
            messages.error(request, 'Form validation failed.')
    else:
        confirm_form = DeleteAllCategoriesForm()

    context = {'confirm_form': confirm_form}
    return render(request, 'delete_all_categories.html', context)

def adding_sub_category(request, slug):
    template = 'sub_category_add.html'
    category = get_object_or_404(Category, slug=slug)
    
    if request.method == 'POST':
        form = Sub_CategoryForm(request.POST, initial={'main_category': category})
        try:
            if form.is_valid():
                new_sub_category = form.save()
                messages.success(request, 'Sub category added successfully!')
                return redirect('services:sub_category_detail', slug=new_sub_category.slug)
        except IntegrityError:
            messages.error(request, 'This slug is already in use. Please choose a different one.')
        except ValidationError as e:
                messages.error(request, f'Validation error: {str(e)}')
        except AttributeError as e:
                messages.error(request, f'Attribute error: {str(e)}')
        except Exception as e:
                messages.error(request, f'Error adding a sub category: {str(e)}')

    else:
        form = Sub_CategoryForm(initial={'main_category': category})

    context = {'form': form, 'category':category}
    return render(request, template, context)
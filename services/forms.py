from django import forms 
from .models import Category, Sub_Category

class CategoryForm(forms.ModelForm):
    confirm_category_addition = forms.BooleanField(required=True, initial=False,
                                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if Category.objects.filter(slug=slug).exists():
            raise forms.ValidationError('This slug is already in use. Please choose a different one.')
        return slug
    
    class Meta:
        model = Category
        fields = ['name', 'category_description', 'slug']
        
class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'category_description', 'slug']

class CategoryDeleteForm(forms.Form):
    confirm_delete = forms.BooleanField(required=True, initial=False,
                                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class DeleteAllCategoriesForm(forms.Form):
    confirm_delete_all = forms.BooleanField(required=True, initial=False,
                                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class Sub_CategoryForm(forms.ModelForm):
    class Meta:
        model = Sub_Category
        fields = ['main_category', 'name', 'sub_Category_description', 'slug']

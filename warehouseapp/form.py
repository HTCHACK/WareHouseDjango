from typing import ClassVar, ForwardRef
from django import forms
from django.db import models
from django.db.models import fields
from .models import Category, Product
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


#Product CRUD FORM
class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category','item_name', 'quantity','cost','phone_number','image','color','issue_by','created_by']


class ProductSearchForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['item_name','export_to_CSV']
        export_to_CSV = forms.BooleanField()

        


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category','item_name', 'quantity','cost','phone_number','image','color','issue_by','created_by']



#CATEGORY CREATEFORM
class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']   


#ISSUE FORM
class IssueForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['issue_quantity','issue_by','issue_to']

class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['recieve_quantity',]

#Reorder Level Form

class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['reorder_level']

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'is_superuser','email', 'password1', 'password2',)
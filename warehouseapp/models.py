from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import DateTimeField, BLANK_CHOICE_DASH

# Create your models here.

STATUS = (
    (0, 'Publish'),
    (1, 'Draft'),
)

COLOR = (
    ('Black', 'Black'),
    ('White', 'White'),
    ('Red', 'Red'),
    ('Gray', 'Gray'),
)

#Products
class Category(models.Model):
    """Category"""
    name = models.CharField(max_length=50, blank=True, null=True)
    #owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name




class Product(models.Model):
    """Product Info"""
    export_to_CSV = models.BooleanField(default=False)

    status = models.IntegerField(choices=STATUS, default=0)
    image = models.ImageField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True,blank=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True, choices=COLOR)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    cost = models.IntegerField(default='0', blank=True, null=True)
    recieve_quantity = models.IntegerField(default='0', blank=True, null=True)
    recieve_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True, default='0')
    issue_by = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, blank=False, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    #owner = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.item_name
    
    @property

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

#class Receive(models.Model):
    #"""Receive item by user"""
    #sender = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name="sender")
    #receiver = models.ManyToManyField(get_user_model(), related_name="receiver")
    #quantity_send = models.ForeignKey(Product, on_delete=models.PROTECT)


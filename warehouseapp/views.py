from django.db.models.query import InstanceCheckMeta, QuerySet
from warehouseapp.models import Product
from django.shortcuts import render, redirect
from .models import *
from .form import *
from django.http import HttpResponse, request, response
import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission,User
from django.utils.translation import gettext as _

# Create your views here.


@login_required(login_url='/login/')
@permission_required('warehouse_app.can_add_data')

def index(request):
    """user = User.objects.create_user(
        username = 'warehouse',
        password = 'aSadbek2000#',
    )
    user.save()"""
    
    return render(request, 'store/index.html')



#---------------------------------------LIST ITEM CRUD----------------------------------------------

@login_required(login_url='/login/')
@permission_required('warehouse_app.can_add_data')
def list_item(request):
    title = "List of Items"
    form = ProductSearchForm(request.POST, request.FILES or None)
    queryset = Product.objects.order_by('-created_on')
    context = {
        'title':title,
        'queryset':queryset,
        'form':form,
        }

    if request.method == 'POST':
	    queryset = Product.objects.filter(item_name__icontains=form['item_name'].value())
	    context = {
        'form':form,
	    "title": title,
	    "queryset": queryset,
                    }

    if form['export_to_CSV'].value()==True:
        response = HttpResponse(content_type = 'text/csv')
        response['Content-Disposition']='attachment : filename="List of product.csv"'
        writer = csv.writer(response)
        writer.writerow(['CATEGORY','ITEM NAME','QUANTITY'])
        instance = queryset
        for product in instance:
            writer.writerow([product.category,product.item_name, product.quantity])
            return response

    return render(request, 'store/list_item.html', context)

#CREATE
@login_required(login_url='/login/')
@permission_required('warehouse_app.can_add_data')
def add_items(request):
    form = ProductCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved')
        return redirect('/admin/list_item')
    

    context = {
        'form': form,
        'title': 'Add Items',
    }
    
    return render(request, 'store/add_items.html', context)

#UPDATE
@login_required(login_url='/login/')
@permission_required('warehouse_app.can_add_data')
def update_items(request, pk):
	queryset = Product.objects.get(id=pk)
	form = ProductUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = ProductUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			return redirect('/admin/list_item')

	context = {
		'form':form
	}
	return render(request, 'store/add_items.html', context)

#DELETE
@login_required(login_url='/login/')
@permission_required('warehouse_app.can_add_data')
def delete_items(request, pk):
	queryset = Product.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		return redirect('/admin/list_item')
	return render(request, 'store/delete_items.html')

#-----------------------------------------CATEGORY CRUD ------------------------------------------------------

@permission_required('warehouse_app.can_add_data')
@login_required(login_url='/login/')
def category_item(request):
    #name = Category.objects.filter(owner=request.user)
    name = Category.objects.all()
    context = {
        'name':name
    }
    return render(request, 'store/category_item.html', context)


   
#add category
@login_required(login_url='/login/')
@permission_required('warehouse_app.can_add_data')
def add_category(request):
    form = CategoryCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Saved Category')
        return redirect('/admin/category_item')
    context = {
        'form': form,
        'title': 'Add Category',
    }

    return render(request, 'store/add_category.html', context)
#update category
@login_required(login_url='/login/')
@permission_required('warehouse_app.can_add_data')
def update_category(request, pk):
	queryset = Category.objects.get(id=pk)
	form = CategoryUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = CategoryUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			return redirect('/admin/category_item')

	context = {
		'form':form
	}
	return render(request, 'store/add_category.html', context)
#delete category
@login_required(login_url='/login/')
@permission_required('warehouse_app.can_add_data')
def delete_category(request, pk):
	queryset = Category.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		return redirect('/admin/category_item')
	return render(request, 'store/delete_category.html')

#PRODUCT DETAIL
@login_required(login_url='/login/')
@permission_required('warehouse_app.can_add_data')
def product_detail(request, pk):
    queryset = Product.objects.get(id=pk)
    context = {
        'queryset':queryset,
    }
    
    return render(request, 'store/product_detail.html', context)



#ISSUE ITEMS
@login_required(login_url='/login/')
@permission_required('warehouse_app.can_add_data')
def issue_items(request, pk):
	queryset = Product.objects.get(id=pk)
	form = IssueForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantity -= instance.issue_quantity

        #instance.issue_by = str(request.user)
		messages.success(request, str(instance.issue_quantity) + " " + str(instance.item_name) +" issued succesfully" + " , " +  'left ' + str(instance.quantity) + " in a Store.")
		instance.save()

		return redirect('/admin/product_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": 'Issue ' + str(queryset.item_name),
		"queryset": queryset,
		"form": form,
		"username": 'Issue By: '+ str(request.user),
	}
	return render(request, "store/add_items.html", context)


@login_required(login_url='/login/')
@permission_required('warehouse_app.can_add_data')
def receive_items(request, pk):
	queryset = Product.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantity += instance.recieve_quantity
		instance.save()
		messages.success(request, str(instance.recieve_quantity) +  " " + str(instance.item_name)+ " received succesfully , totall = " + str(instance.quantity) + " in a Store.")

		return redirect('/admin/product_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
	context = {
			"title": 'Reaceive ' + str(queryset.item_name),
			"instance": queryset,
			"form": form,
			"username": 'Receive By: ' + str(request.user),
		}
	return render(request, "store/add_items.html", context)
  

#REORDER LEVEL
@login_required(login_url='/login/')
@permission_required('warehouse_app.can_add_data')
def reorder_level(request, pk):
    """Reorder level"""
    queryset = Product.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))

        return redirect('/admin/list_item')
    context = {
            'instance':queryset,
            'form':form,
    }
    return render(request, 'store/add_items.html', context) 


#user
@login_required(login_url='/login/')
#@permission_required('warehouse_app.can_add_data')
def user_list(request):
    user = User.objects.all()
    context = {
        'title' : "User List",
        'user':user,
    }
    return render(request, 'store/user_list.html',context)

@login_required(login_url='/login/')
#@permission_required('warehouse_app.can_add_data')
def add_user(request):
    form = SignUpForm(data=request.POST)
    if form.is_valid():
        form.save()
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        username = form.cleaned_data.get('username')
        is_superuser = form.cleaned_data.get('is_superuser')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(first_name=first_name,last_name=last_name, username=username,is_superuser=is_superuser, email=email, password=password)
        login(request, user)
        messages.success(request, 'Successfully Added')
        return redirect('/admin/user_list')


    context = {
        'form': form,
        'title': 'Add Worker',
    }
    
    return render(request, 'store/add_user.html', context)
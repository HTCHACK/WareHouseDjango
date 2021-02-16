from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from . import views

app_name = 'store'
            
urlpatterns = [
    path('', views.index, name='index'),
    path('list_item/', views.list_item, name='list_item'),
    path('add_items/', views.add_items, name='add_items'),
    path('update_items/<str:pk>/', views.update_items, name="update_items"),
    path('delete_items/<str:pk>/', views.delete_items, name="delete_items"),
    path('category_item/', views.category_item, name='category_item'),
    path('add_category/',views.add_category, name='add_category'),
    path('update_category/<str:pk>/', views.update_category , name='update_category'),
    path('delete_category/<str:pk>/', views.delete_category, name='delete_category'),
    path('product_detail/<str:pk>/', views.product_detail, name='product_detail'),
    path('issue_items/<str:pk>/', views.issue_items, name="issue_items"),
    path('receive_items/<str:pk>/', views.receive_items, name="receive_items"),
    path('reorder_level/<str:pk>/', views.reorder_level, name='reorder_level'),  
    path('user_list/', views.user_list, name='user_list'),
    path('add_user/', views.add_user, name='add_user'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
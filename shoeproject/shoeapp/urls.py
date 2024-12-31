
from django.urls import path
from .views import *  

urlpatterns = [
    path('', home,name='home'),  
    # Supplier
    path('register_supplier/', register_supplier, name='register_supplier'),
     path('supplier_dashboard/', supplier_dashboard, name='supplier_dashboard'),

    # User
    path('register_user/', register_user, name='register_user'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),

    # Common
    path('login/', login_view, name='login'),

    # Admin
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
   
    
]

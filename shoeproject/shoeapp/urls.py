
from django.urls import path
from .views import *  

urlpatterns = [
    path('', home,name='home'),  
    # Supplier
    path('register_supplier/', register_supplier, name='register_supplier'),
    path('supplier_dashboard/', supplier_dashboard, name='supplier_dashboard'),
    path('add-category/', add_category, name='add_category'),
    path('update-category/<int:category_id>/', update_category, name='update_category'),
    path('delete-category/<int:category_id>/', delete_category, name='delete_category'),
    path('add-product/', add_product, name='add_product'),
    path('update-product/<int:product_id>/', update_product, name='update_product'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('view-categories/', view_all_categories, name='view_all_categories'),
    path('view-products/', view_all_products, name='view_all_products'),

    # User
    path('register_user/', register_user, name='register_user'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),

    # Common
    path('login/', login_view, name='login'),

    # Admin
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('approve_user/<int:user_id>/', approve_user, name='approve_user'),
    path('approve_supplier/<int:supplier_id>/', approve_supplier, name='approve_supplier'),
    path('view_all_users/', view_all_users, name='view_all_users'),
    path('view_all_suppliers/', view_all_suppliers, name='view_all_suppliers'),
    path('update_user/<int:user_id>/', update_user, name='update_user'),
    path('update_supplier/<int:supplier_id>/', update_supplier, name='update_supplier'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('delete_supplier/<int:supplier_id>/', delete_supplier, name='delete_supplier'),
    
]

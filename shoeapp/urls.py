
from django.urls import path
from .views import * 
from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path('', index,name='home'),  
    path('', index,name='index'),  
    # Supplier
    path('register_supplier/', register_supplier, name='register_supplier'),
    path('supplier_dashboard/', supplier_dashboard, name='supplier_dashboard'),
    path('view_products/', view_products, name='view_products'),
    path('update_product_supplier/<int:product_id>/', update_product_supplier, name='update_product_supplier'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/', remove_from_cart, name='remove_from_cart'),
    path('search/', search_view, name='search'),
    path('update_supplier_profile/', update_supplier_profile, name='update_supplier_profile'),
    path('supplier_profile/', supplier_profile, name='supplier_profile'),

    # User
    path('register_user/', register_user, name='register_user'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('cart/', view_cart, name='view_cart'),
    path('categories/', view_categories, name='view_categories'),
    path('category/<int:category_id>/', view_products_by_category, name='view_products_by_category'),
    path('update_profile/', update_profile, name='update_profile'),
    path('view_profile/', view_profile, name='view_profile'),


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
    path('add-category/', add_category, name='add_category'),
    path('update-category/<int:category_id>/', update_category, name='update_category'),
    path('delete-category/<int:category_id>/', delete_category, name='delete_category'),
    path('add-product/', add_product, name='add_product'),
    path('update-product/<int:product_id>/', update_product, name='update_product'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('view-categories/', view_all_categories, name='view_all_categories'),
    path('view-products/', view_all_products, name='view_all_products'),
    path('logout/', user_logout, name='logout'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ProductSitemap







sitemaps = {
    'products': ProductSitemap,
}



urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:id>', views.detail, name='detail'),
    path('success/', views.payment_success_view,name='success'),
    path('failed', views.payment_failed_view,name='failed'),
    path('api/checkout-session/<int:id>/', views.create_checkout_session,  name='api_checkout_session'),
    # path('register/', views.register, name='register'),
    # path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    # path('logout/', views.custom_logout_view, name='logout'),
    path('purchases/', views.my_purchases, name='purchases'),
    path('analytics', views.analytics, name='analytics'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]



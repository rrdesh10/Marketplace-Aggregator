from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:id>', views.detail, name='detail'),
    path('done/', views.payment_success_view, name='done'),
    path('failed', views.payment_failed_view, name='failed'),
    path('api/checkoutsession/<int:id>', views.create_checkout_session, name='api_checkout_session'),
    path('create', views.create_product, name='create'),
    path('edit/<int:id>', views.edit_product, name='edit'),
    path('delete/<int:id>', views.delete_product, name='delete'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('register', views.register_view, name='register'),
    path('login', LoginView.as_view(template_name='mkpa_app/login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='mkpa_app/logout.html'), name='logout'),
]
from django.urls import path
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
]
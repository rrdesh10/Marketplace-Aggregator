from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponseNotFound
from .models import Product, OrderDetail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import stripe


def index(request):
    products = Product.objects.all()
    return render(request, 'mkpa_app/index.html', {'products':products})


def detail(request, id):
    product = Product.objects.get(id=id)
    stripe_pub_key = settings.STRIPE_PUBLISHABLE_KEY
    return render(request, 'mkpa_app/detail.html', {'product':product, 'stripe_pub_key':stripe_pub_key})


@csrf_exempt
def create_checkout_session(request, id):
    request_data = json.loads(request.body)
    product = Product.objects.get(id=id)
    stripe.api_key = settings.STRIPE_SECERT_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email = request.user.email,
        payment_method_types = ['card'],
        line_items = [
            {
                'price_data':{
                    'currency':'inr',
                    'product_data':{'name':product.name,},
                    'unit_amount':int(product.price * 100)
                },
                'quantity':1,
            }
        ],
        mode ='payment',
        success_url = request.build_absolute_uri(reverse('success'))+
        '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url = request.build_absolute_uri(reverse('failed')),
    )

    order = OrderDetail()
    order.customer_email = request_data['email']
    order.product = product 
    order.amount = int(product.price)
    order.stripe_payment_intent = 'Rohit'
    order.save()

    return JsonResponse({'sessionId':checkout_session.id})


def payment_success_view(request):
    session_id = request.Get.get('session_id')
    if session_id is None:
        return HttpResponseNotFound()
    stripe.api_key = settings.STRIPE_SECERT_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    order = get_object_or_404(OrderDetail, stripe_payment_intent = session.payment_intent)
    order.has_paid = True
    order.save()

    return render(request, 'mkpa_app/payment_success.html', {'order':order})


def payment_failed_view(request):
    return render(request, 'mkpa_app/payment_failed.html')

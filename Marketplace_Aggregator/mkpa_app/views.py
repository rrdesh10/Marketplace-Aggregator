from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponseNotFound
from .models import Product, OrderDetail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .forms import ProductForm, RegistrationForm
import stripe, json


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
        success_url = request.build_absolute_uri(reverse('done'))+
        '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url = request.build_absolute_uri(reverse('failed')),
    )

    order = OrderDetail()
    order.customer_email = request_data['email']
    order.product = product 
    order.amount = int(product.price)
    order.stripe_payment_intent = checkout_session['id']
    order.save()

    return JsonResponse({'sessionId':checkout_session.id})


def payment_success_view(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
        return HttpResponseNotFound()
    stripe.api_key = settings.STRIPE_SECERT_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    order = get_object_or_404(OrderDetail, stripe_payment_intent = session.id)
    order.has_paid = True
    order.save()

    return render(request, 'mkpa_app/payment_success.html', {'order':order})


def payment_failed_view(request):
    return render(request, 'mkpa_app/payment_failed.html')


def create_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            new_product = product_form.save()
            return redirect('index')

    product_form = ProductForm()
    return render(request, 'mkpa_app/create_product.html', {'product_form':product_form})


def edit_product(request, id):
    product = Product.objects.get(id=id)
    product_form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if request.method == "POST":
        if product_form.is_valid():
            product_form.save()
            return redirect('index')

    return render(request, 'mkpa_app/edit_product.html', {'product_form':product_form, 'product':product})


def delete_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        product.delete()
        return redirect('index')
    return render(request, 'mkpa_app/delete_product.html', {'product':product})


def dashboard(request):
    products = Product.objects.all()
    return render(request, 'mkpa_app/dashboard.html', {'products':products})


def register_view(request):
    if request.method == "POST":
        register_form = RegistrationForm(request.POST)
        new_user = register_form.save(commit=False)
        new_user.set_password(register_form.cleaned_data['password'])
        new_user.save()
        return redirect('login')

    register_form = RegistrationForm()
    return render(request, 'mkpa_app/register.html', {'register_form':register_form})
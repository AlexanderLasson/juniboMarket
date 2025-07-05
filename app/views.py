from django.shortcuts import render, get_object_or_404
from .models import Product, OrderDetail
from django.conf import settings
import stripe, json
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse, HttpResponseNotFound
import logging
from  .forms import UserRegistrationForm
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail


def index(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        purchased_products = OrderDetail.objects.filter(customer_email=request.user.email, has_paid=True).values_list('product_id', flat=True)
    else:
        purchased_products = []
    return render(request, 'app/index.html', {'products': products, 'purchased_products': purchased_products})

@login_required
def index2(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        purchased_products = OrderDetail.objects.filter(customer_email=request.user.email, has_paid=True).values_list('product_id', flat=True)
    else:
        purchased_products = []
    return render(request, 'app/index.html', {'products': products, 'purchased_products': purchased_products})

def detail(request, id):
    product = Product.objects.get(id=id)
    stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
    return render(request, 'app/detail.html',{'product':product, 'stripe_publishable_key':stripe_publishable_key, 'request':request})


logger = logging.getLogger(__name__)

import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def create_checkout_session(request,id):
    request_data = json.loads(request.body)
    product = Product.objects.get(id=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email = request_data['email'],
        payment_method_types = ['card'],
        line_items=[
            {
                'price_data':{
                    'currency':'usd',
                    'product_data':{
                        'name':product.name,
                    },
                    'unit_amount':int(product.price * 100)
                },
                'quantity':1,
            }
        ],
        mode='payment',
        success_url = request.build_absolute_uri(reverse('success')) +
        "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(reverse('failed')),

    )

    order = OrderDetail()
    order.customer_email = request_data['email']
    order.product = product
    order.stripe_payment_intent = checkout_session['id']
    order.amount = int(product.price)
    order.save()

    return JsonResponse({'sessionId':checkout_session.id})

@login_required
def payment_success_view(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
        return HttpResponseNotFound()
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    order = get_object_or_404(OrderDetail, stripe_payment_intent=session.id)

    # This updates the id to payment_intent due to stripe api update
    order.stripe_payment_intent = session['payment_intent']
    order.has_paid = True
    # for updating sales stats for a product
    product = Product.objects.get(id=order.product.id)
    product.total_sales_amount = product.total_sales_amount + int(product.price)
    product.total_orders = product.total_orders + 1
    product.save()
    order.save()

    subject = 'Thank You for Your Purchase'
    message = (
    f"Dear {order.customer_email},\n\n"
    f"Thank you for your purchase from Junibo! "
    f"We're excited to confirm your order of {order.product.name}. "
    f"Your payment has been successfully processed, and your digital wallpaper "
    f"is now available for download in your backgrounds page.\n\n"
    f"If you have any questions or need further assistance, feel free to contact "
    f"us.\n\n"
    f"Best regards,\n"
    f"The Junibo Team"
)
    from_email = settings.EMAIL_HOST_USER
    to_email = order.customer_email  
    send_mail(subject, message, from_email, [to_email])


    return render(request, 'app/payment_success.html', {'order': order})


def payment_failed_view(request):
    return render(request, 'app/failed.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        return redirect('index')

    user_form = UserRegistrationForm
    return render(request, 'app/register.html', {'user_form':user_form})


def custom_logout_view(request):
    logout(request)
    return render(request, 'app/logout.html')


@login_required
def my_purchases(request):
    orders = OrderDetail.objects.filter(customer_email=request.user.email, has_paid=True)
    purchased_products = [order.product for order in orders]
    return render(request, 'app/purchases.html', {'orders': orders, 'purchased_products': purchased_products})


def is_admin(user):
    return user.is_staff or user.is_superuser

# custom admin verification for dashboard analytics
@user_passes_test(is_admin)
def analytics(request):
    total_orders = OrderDetail.objects.aggregate(Sum('amount'))

    product_sales_sums = OrderDetail.objects.values('product__name').annotate(sum=Sum('amount')).order_by('-sum')
    return render(request, 'app/analytics.html', {
        'total_sales': total_orders,
        'product_sales_sums': product_sales_sums,
    })

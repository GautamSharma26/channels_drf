from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializer import *
from .models import *
from .permission import IsOwner
from rest_framework.response import Response
from .tasks import mail_send
from django.shortcuts import render, redirect
from pizza.message import *
from django.conf import settings
import stripe
from .stripe_utils import stripe_session_create, stripe_customer_create


class PizzaAdminView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.all()

    def destroy(self, request, *args, **kwargs):
        data = kwargs['pk']
        data_pizza = Pizza.objects.get(id=data)
        pizza_data = CartPizza.objects.filter(pizza_id=data).first()
        order_pizza = OrderPizza.objects.filter(pizza_id=data).first()
        if pizza_data or order_pizza:
            """
            Here it is checking for pizza id is present or not in cart and order.
            If present then simply change it to is_deleted = true.
            If not present then delete it .
            """
            data_pizza.is_deleted = True
            data_pizza.save()
            return Response({delete})
        data_pizza.delete()
        return Response({delete})

    def partial_update(self, request, *args, **kwargs):
        super(PizzaAdminView, self).partial_update(request, *args, **kwargs)
        return Response({update})


class PizzaAllView(viewsets.ModelViewSet):
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.all()


class AddressView(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    serializer_class = AddressSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        queryset = Address.objects.filter(user=user)
        return queryset


class AddressWrite(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = AddressWriteSerializer
    queryset = Address.objects.all()
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        super(AddressWrite, self).destroy(request, *args, **kwargs)
        return Response({delete})

    def partial_update(self, request, *args, **kwargs):
        super(AddressWrite, self).partial_update(request, *args, **kwargs)
        return Response({update})


class AddressCreate(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = AddressWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data})
        return Response({'error': serializer.errors})


class CartView(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsOwner]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        cart = Cart.objects.filter(user=user)
        return cart

    def create(self, request, *args, **kwargs):
        user = self.request.user
        data = request.data
        cart, _ = Cart.objects.get_or_create(user=user)
        pizza_id_data = data.get('pizza')
        pizza_data = Pizza.objects.filter(id=pizza_id_data, is_deleted=False).first()
        if pizza_data:
            CartPizza.objects.create(pizza_id=data.get('pizza'), cart=cart, quantity=data.get('quantity'))
            return Response({create})
        return Response({no_pizza})


class CartPizzaView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartPizzaSerializer
    queryset = CartPizza.objects.all()
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        super(CartPizzaView, self).destroy(self, request, *args, **kwargs)
        return Response({delete})


class OrderCreate(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        address = Address.objects.filter(id=data.get('address'), user=user).first()
        if address:
            cart = Cart.objects.filter(user=user).first()
            if cart.total_amount > 0:
                self.check_object_permissions(request, cart)
                data['total_amount'] = cart.total_amount
                serializer = OrderSerializer(data=data, context={"request": request})
                if serializer.is_valid(raise_exception=True):
                    order = serializer.save()
                    mail_send.delay("Order done", order.user.email, "Order of Pizza")
                    for pizza_data in CartPizza.objects.filter(cart=cart):
                        OrderPizza.objects.create(order_id=order.id, pizza=pizza_data.pizza,
                                                  price=pizza_data.pizza.price,
                                                  quantity=pizza_data.quantity,
                                                  total_amount=pizza_data.total_amount)
                    metadata = {
                        'id': serializer.data.get('id'),
                        'user': serializer.data.get('user')

                    }
                    pay_data = {
                        "price_data": {
                            "currency": "inr",
                            "unit_amount": int(cart.total_amount) * 100,
                            "product_data": {
                                "name": cart,
                                "metadata": metadata,
                            },
                        },
                        "quantity": 1
                    }
                    session = stripe_session_create(pay_data)
                    stripe_customer_create(user, cart)
                    cart.pizza.clear()  # this is used clear all data from its associate table
                    cart.total_amount = 0
                    cart.save()
                    # invoice_sender(items, cart, user)
                    return Response({session.url, create})
                return Response({no_order})
            return Response({no_items})
        return Response({no_address})


def login_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            if not user.is_delivery_boy:
                return redirect('home')
            else:
                return redirect('order-delivered')
        else:
            return redirect('/')
    else:
        messages.error(request, 'invalid form data')
    return render(request, 'login.html')


def order_status(request, order_idd):
    order = Order.objects.get(user=request.user, order_idd=order_idd)
    if order:
        context = {'order': order}
    else:
        context = {'order': "1"}
    return render(request, 'order.html', context)


def home(request):
    order = Order.objects.filter(user=request.user)
    if order:
        context = {'order': order}
    else:
        context = {'order': "1"}
    return render(request, 'home.html', context)


def success_payment(request):
    return render(request, 'success.html')


def cancel_payment(request):
    return render(request, 'cancel.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        payment_intent = stripe.checkout.Session.list(
            payment_intent=session["payment_intent"],
            expand=['data.line_items']
        )
        product_id = payment_intent['data'][0]['line_items']['data'][0]['price']['product']
        product = stripe.Product.retrieve(product_id)
        order_id = product['metadata']['id']
        order_obj = Order.objects.filter(id=order_id).first()
        if session.payment_status == "paid":
            order_obj.is_payed = True
            order_obj.save()
    return HttpResponse(status=200)


def order_delivered(request):
    return render(request, 'order_delivered.html')


def order_delivered_url(request, id):
    # DeliveryBoy.objects.create(delivery_boy=request.user,order_id=id)
    order_data = Order.objects.filter(id=id).first()
    delivery_boy = DeliveryBoy.objects.filter(order_id=id).first()
    if not delivery_boy:
        serializer = DeliveryBoySerializer(data={
            'order_id': id
        }, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            order_data.is_delivered = True
            order_data.save()
            return HttpResponse(f"Order Accepted of {request.user}")
    return HttpResponse("Order already accepted")

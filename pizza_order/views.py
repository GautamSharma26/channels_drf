from django.contrib import messages
from django.contrib.auth import authenticate, login
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializer import *
from .models import *
from .permission import IsOwner
from rest_framework.response import Response
from .signals import send_mail_func
from django.shortcuts import render, redirect
from pizza.message import *


class PizzaAdminView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.all()

    def destroy(self, request, *args, **kwargs):
        super(PizzaAdminView, self).destroy(request, *args, **kwargs)
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
    permission_classes = [IsAuthenticated,]
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
        address = Address.objects.get(id=data.get('address'))
        if address:
            cart = Cart.objects.filter(user=user).first()
            if cart.total_amount > 0:
                self.check_object_permissions(request, cart)
                data['total_amount'] = cart.total_amount
                serializer = OrderSerializer(data=data, context={"request": request})
                if serializer.is_valid(raise_exception=True):
                    order = serializer.save()
                    send_mail_func(order)
                    for pizza_data in CartPizza.objects.filter(cart=cart):
                        OrderPizza.objects.create(order_id=order.id, pizza=pizza_data.pizza,
                                                  price=pizza_data.pizza.price, quantity=pizza_data.quantity,
                                                  total_amount=pizza_data.total_amount)
                    cart.pizza.clear()  # this is used clear all data from its associate table
                    cart.total_amount = 0
                    cart.save()
                    return Response({create})
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
            return redirect('home')
        else:
            return redirect('/')
    else:
        messages.error(request, 'invalid form data')
    return render(request, 'login.html')


def order_status(request, order_idd):
    order = Order.objects.filter(user=request.user, order_idd=order_idd).first()
    if order:
        context = {'order': order}
    else:
        context = {'order': "1"}
    return render(request, 'order.html', context)


def home(request):
    order = Order.objects.filter(user=request.user).first()
    if order:
        context = {'order': order}
    else:
        context = {'order': "1"}
    return render(request, 'home.html', context)

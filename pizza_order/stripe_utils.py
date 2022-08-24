import stripe
from django.conf import settings


def stripe_session_create(data):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[data],
        mode='payment',
        success_url=f"{settings.DOMAIN}product/success",
        cancel_url=f"{settings.DOMAIN}product/cancel",
    )
    return session


def stripe_customer_create(user, cart):
    customer = stripe.Customer.create(
                        name=user.first_name,
                        email=user.email,
                    )
    stripe.PaymentIntent.create(
        customer=customer.id,
        receipt_email=customer.email,
        payment_method_types=['card'],
        currency="inr",
        setup_future_usage='off_session',
        amount=int(cart.total_amount * 100),

    )

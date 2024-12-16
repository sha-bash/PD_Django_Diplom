from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from backend.models import ConfirmEmailToken, Order, User
from easy_thumbnails.files import generate_all_aliases

@shared_task
def send_password_reset_email(reset_password_token_key):
    try:
        reset_password_token = ConfirmEmailToken.objects.get(key=reset_password_token_key)
        user = reset_password_token.user
        msg = EmailMultiAlternatives(
            f"Password Reset Token for {user.email}",
            reset_password_token.key,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        msg.send()
    except ConfirmEmailToken.DoesNotExist:
        print(f"Invalid password reset token: {reset_password_token_key}")

@shared_task
def send_registration_email(user_id):
    user = User.objects.get(id=user_id)
    token, _ = ConfirmEmailToken.objects.get_or_create(user=user)
    msg = EmailMultiAlternatives(
        f"Registration Confirmation for {user.email}",
        token.key,
        settings.EMAIL_HOST_USER,
        [user.email]
    )
    msg.send()

@shared_task
def generate_thumbnails(pk, model, field):
    instance = model.objects.get(pk=pk)
    generate_all_aliases(instance, field)

@shared_task
def send_order_notification(user_id, order_id):
    user = User.objects.get(id=user_id)
    order = Order.objects.get(id=order_id)
    msg = EmailMultiAlternatives(
        f"Order Confirmation for {user.email}",
        f"Your order {order.id} has been placed.",
        settings.EMAIL_HOST_USER,
        [user.email]
    )
    msg.send()
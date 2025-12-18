from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail


def send_account_activation_email(email, email_token):
    subject = "Your account needs to be verified"
    email_from = settings.EMAIL_HOST_USER
    message = f'Click on the link to activate your account http://127.0.0.1:8000/accounts/activate/{email_token}'
    send_mail(subject, message, email_from, [email])


def send_invoice_email(email, payment):
    """Send invoice PDF via email"""
    subject = f"Invoice for Order #{payment.razorpay_order_id}"
    email_from = settings.EMAIL_HOST_USER
    message = f"""
    Thank you for your purchase!
    
    Your order has been confirmed.
    Order ID: {payment.razorpay_order_id}
    Payment ID: {payment.razorpay_payment_id}
    Amount: ₹{payment.amount/100}
    
    Please find your invoice attached.
    
    Thank you for shopping with us!
    """
    
    email_msg = EmailMessage(
        subject,
        message,
        email_from,
        [email]
    )
    
    # Attach PDF if exists
    if payment.invoice_pdf:
        email_msg.attach_file(payment.invoice_pdf.path)
    
    email_msg.send()
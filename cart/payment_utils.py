import razorpay
from django.conf import settings
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from django.core.files.base import ContentFile


def get_razorpay_client():
    """Get Razorpay client instance"""
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def create_razorpay_order(amount, receipt_id, notes=None):
    """Create a Razorpay order"""
    client = get_razorpay_client()
    order = client.order.create({
        'amount': amount,  # Amount in paise
        'currency': 'INR',
        'receipt': receipt_id,
        'notes': notes or {}
    })
    return order


def verify_payment_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    """Verify payment signature from Razorpay"""
    client = get_razorpay_client()
    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    }
    try:
        client.utility.verify_payment_signature(params_dict)
        return True
    except razorpay.errors.SignatureVerificationError:
        return False


def generate_invoice_pdf(payment):
    """Generate PDF invoice for payment"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Title
    elements.append(Paragraph("INVOICE", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Company Info
    company_info = [
        ['Invoice Number:', f'INV-{payment.uid}'],
        ['Date:', payment.create_at.strftime('%d/%m/%Y %H:%M')],
        ['Order ID:', payment.razorpay_order_id],
        ['Payment ID:', payment.razorpay_payment_id or 'N/A'],
        ['Status:', payment.status],
    ]
    
    company_table = Table(company_info, colWidths=[2*inch, 4*inch])
    company_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(company_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Customer Info
    cart = payment.cart
    customer_name = cart.user.get_full_name() if cart.user else 'Guest User'
    customer_email = cart.user.email if cart.user else 'N/A'
    
    customer_info = [
        ['Bill To:'],
        ['Name:', customer_name],
        ['Email:', customer_email],
    ]
    
    customer_table = Table(customer_info, colWidths=[2*inch, 4*inch])
    customer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (0, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(customer_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Items Table
    cart_items = cart.cart_items.all()
    items_data = [['Product', 'Size', 'Color', 'Quantity', 'Price']]
    
    for item in cart_items:
        product_name = item.product.product_name if item.product else 'Deleted Product'
        size = item.size_variant.size if item.size_variant else 'N/A'
        color = item.color_variant.color_name if item.color_variant else 'N/A'
        quantity = item.quantity
        price = item.get_product_price()
        items_data.append([product_name, size, color, str(quantity), f'₹{price}.00'])
    
    items_table = Table(items_data, colWidths=[2.5*inch, 1*inch, 1*inch, 0.8*inch, 1.2*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Totals
    subtotal = cart.get_cart_total()
    discount = cart.get_discount_amount()
    total = cart.get_cart_total_after_discount()
    
    totals_data = [
        ['Subtotal:', f'₹{subtotal}.00'],
    ]
    
    if discount > 0:
        totals_data.append(['Discount:', f'-₹{discount}.00'])
    
    totals_data.append(['Total:', f'₹{total}.00'])
    
    totals_table = Table(totals_data, colWidths=[4*inch, 2*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('FONTSIZE', (-1, -1), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (-1, -1), (-1, -1), 12),
    ]))
    elements.append(totals_table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    # Save to file
    filename = f'invoice_{payment.uid}.pdf'
    payment.invoice_pdf.save(filename, ContentFile(buffer.read()), save=True)
    buffer.close()
    
    return payment.invoice_pdf


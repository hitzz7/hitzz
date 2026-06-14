from io import BytesIO
import os

from PIL import Image, ImageDraw, ImageFont

from .models import InvoiceItem


def _font(size, bold=False):
    candidates = []
    if os.name == 'nt':
        candidates.append(
            'C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf'
        )
    candidates.extend([
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf',
    ])
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def generate_invoice_png(invoice):
    items = list(invoice.items.all())
    width = 900
    padding = 48
    line_h = 28
    y = padding

    # Estimate height
    height = padding * 2 + 220 + len(items) * 36 + 180
    if invoice.notes:
        height += 80

    img = Image.new('RGB', (width, height), '#ffffff')
    draw = ImageDraw.Draw(img)

    title_font = _font(36, bold=True)
    heading_font = _font(14, bold=True)
    body_font = _font(13)
    small_font = _font(12)
    total_font = _font(16, bold=True)

    orange = '#ffa500'
    dark = '#222222'
    gray = '#666666'
    light_gray = '#eeeeee'

    # Header
    draw.text((padding, y), 'INVOICE', fill=orange, font=title_font)
    draw.text((width - padding - _text_width(draw, invoice.invoice_number, heading_font), y),
              invoice.invoice_number, fill=dark, font=heading_font)
    y += 50

    draw.text((padding, y), 'Hitzz', fill=dark, font=heading_font)
    y += line_h
    draw.text((padding, y), 'Web Design & Development', fill=gray, font=body_font)
    y += line_h
    draw.text((padding, y), 'Nepal', fill=gray, font=body_font)

    meta_x = width - padding - 200
    meta_y = padding + 50
    for label, value in [
        ('Issue Date', str(invoice.issue_date)),
        ('Due Date', str(invoice.due_date)),
        ('Status', invoice.get_status_display()),
    ]:
        draw.text((meta_x, meta_y), f'{label}: {value}', fill=gray, font=small_font)
        meta_y += 22

    y = max(y, meta_y) + 30

    # Bill to
    draw.text((padding, y), 'BILL TO', fill=gray, font=small_font)
    y += 22
    draw.text((padding, y), invoice.client_name, fill=dark, font=heading_font)
    y += line_h
    if invoice.client_email:
        draw.text((padding, y), invoice.client_email, fill=gray, font=body_font)
        y += line_h
    if invoice.client_address:
        for line in invoice.client_address.splitlines():
            draw.text((padding, y), line, fill=gray, font=body_font)
            y += line_h

    y += 20

    # Table header
    col_desc = padding
    col_qty = width - padding - 280
    col_price = width - padding - 180
    col_total = width - padding - 80

    draw.rectangle([padding, y, width - padding, y + 36], fill=orange)
    draw.text((col_desc + 8, y + 10), 'Description', fill='#ffffff', font=heading_font)
    draw.text((col_qty, y + 10), 'Qty', fill='#ffffff', font=heading_font)
    draw.text((col_price, y + 10), 'Unit Price', fill='#ffffff', font=heading_font)
    draw.text((col_total, y + 10), 'Amount', fill='#ffffff', font=heading_font)
    y += 36

    for item in items:
        draw.line([padding, y + 35, width - padding, y + 35], fill=light_gray)
        desc = item.description[:40]
        if item.item_type != InvoiceItem.TYPE_CHARGE:
            label = item.get_type_display_short()[:12]
            desc = f'[{label}] {desc}'[:50]
        draw.text((col_desc + 8, y + 10), desc, fill=dark, font=body_font)
        draw.text((col_qty, y + 10), str(item.quantity), fill=dark, font=body_font)
        draw.text((col_price, y + 10), f'Rs. {item.unit_price}', fill=dark, font=body_font)
        draw.text((col_total, y + 10), f'Rs. {item.line_total}', fill=dark, font=body_font)
        y += 36

    y += 20
    totals_x = width - padding - 260

    def draw_total_row(label, value, bold=False):
        nonlocal y
        font = total_font if bold else body_font
        draw.text((totals_x, y), label, fill=dark, font=font)
        draw.text((width - padding - _text_width(draw, value, font), y), value, fill=dark, font=font)
        y += 30

    draw_total_row('Subtotal', f'Rs. {invoice.subtotal}')
    if invoice.tax_rate:
        draw_total_row(f'Tax ({invoice.tax_rate}%)', f'Rs. {invoice.tax_amount}')
    draw.line([totals_x, y, width - padding, y], fill=dark, width=2)
    y += 12
    draw_total_row('Total', f'Rs. {invoice.total}', bold=True)

    if invoice.advance_paid:
        draw_total_row('Advance Paid', f'- Rs. {invoice.advance_paid}')
    draw_total_row('Balance Due', f'Rs. {invoice.balance_due}', bold=True)

    if invoice.notes:
        y += 10
        draw.text((padding, y), 'Notes:', fill=dark, font=heading_font)
        y += 22
        for line in invoice.notes.splitlines():
            draw.text((padding, y), line, fill=gray, font=body_font)
            y += line_h

    # Crop to actual content height
    img = img.crop((0, 0, width, min(y + padding, height)))

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

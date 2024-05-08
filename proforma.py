from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

def generate_invoice(invoice_info, items, filename):
    # Create a canvas
    # c = canvas.Canvas(filename, pagesize=letter)
    invoice_width = A4[0] / 2
    invoice_height = A4[1] / 2
    c = canvas.Canvas(filename, pagesize=(invoice_width, invoice_height))

    # Set up the invoice information
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, "Invoice")
    c.drawString(50, 730, "Distributor Name: {}".format(invoice_info['distributor_name']))
    c.drawString(50, 710, "Invoice Number: {}".format(invoice_info['invoice_number']))
    c.drawString(50, 690, "Date: {}".format(invoice_info['date']))

    # Draw a line under the invoice information
    c.line(50, 680, 550, 680)

    # Set up the table headers
    c.drawString(50, 660, "Item")
    c.drawString(200, 660, "Quantity")
    c.drawString(300, 660, "Price")
    c.drawString(400, 660, "Total")

    # Draw a line under the table headers
    c.line(50, 650, 550, 650)

    # Set up the items
    y_position = 630
    total_amount = 0
    for item in items:
        c.drawString(50, y_position, item['name'])
        c.drawString(200, y_position, str(item['quantity']))
        c.drawString(300, y_position, "${:.2f}".format(item['price']))
        total = item['quantity'] * item['price']
        c.drawString(400, y_position, "${:.2f}".format(total))
        total_amount += total
        y_position -= 20

    # Draw a line above the total
    c.line(50, y_position, 550, y_position)

    # Print the total
    c.drawString(50, y_position - 20, "Total: ${:.2f}".format(total_amount))

    # Save the PDF
    c.save()

# Example usage
invoice_info = {
    'distributor_name': 'ABC Distributors',
    'invoice_number': 'INV-001',
    'date': '2024-05-05'
}

items = [
    {'name': 'Product A', 'quantity': 2, 'price': 10},
    {'name': 'Product B', 'quantity': 3, 'price': 15},
    {'name': 'Product C', 'quantity': 1, 'price': 20}
]

generate_invoice(invoice_info, items, 'invoice.pdf')

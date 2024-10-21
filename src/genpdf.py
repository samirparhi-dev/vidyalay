from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg

def generate_pdf_from_svgs(output_pdf, svg_files):
    c = canvas.Canvas(output_pdf, pagesize=(595.28, 841.89))  # A4 size in points
    width, height = 595.28, 841.89
    card_width, card_height = 560, 590  # Card dimensions in points
    gap = 2.83465  # 1 mm gap in points

    cards_per_page = 4  # 2 rows and 2 columns per page
    
    # Calculate x and y positions considering the gap
    x_positions = [gap, width / 2 - card_width / 2]  # Two columns (left, right)
    y_positions = [height - gap - card_height, height / 2 - gap - card_height]  # Two rows (top, bottom)

    for i, svg_file in enumerate(svg_files):
        # Add a new page after every 4 cards
        if i % cards_per_page == 0 and i > 0:
            c.showPage()

        # Calculate the position of the current card on the A4 layout
        card_index_on_page = i % cards_per_page
        x_pos = x_positions[card_index_on_page % 2]  # Two columns (left or right)
        y_pos = y_positions[card_index_on_page // 2]  # Two rows (top or bottom)

        # Load the SVG as a drawing
        drawing = svg2rlg(svg_file)
        drawing.scale(card_width / drawing.width, card_height / drawing.height)  # Scale to fit the card

        # Draw the SVG card at the calculated position
        renderPDF.draw(drawing, c, x_pos, y_pos)

    print(f"PDF generated: {output_pdf}")
    c.save()

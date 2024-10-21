from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg

def generate_pdf_from_svgs(output_pdf, svg_files):
    c = canvas.Canvas(output_pdf, pagesize=(595.28, 841.89))  # A4 size in points (Portrait)
    width, height = 595.28, 841.89  # A4 dimensions
    gap = 2.83465  # 1 mm gap in points for borders

    # Card dimensions
    card_width = (width - 3 * gap) / 2  # Two columns: Left and right, with gap between
    card_height = (height - 3 * gap) / 2  # Two rows: Top and bottom, with gap between

    cards_per_page = 4  # 4 cards per page (2 columns x 2 rows)

    # x_positions for 2 columns (left and right) and y_positions for 2 rows (top and bottom)
    x_positions = [gap, width / 2 + gap / 2]  # Two columns: left and right
    y_positions = [height - gap - card_height, (height / 2) - (card_height / 2)]  # Two rows: top and bottom

    for i, svg_file in enumerate(svg_files):
        # Add a new page after every 4 cards
        if i % cards_per_page == 0 and i > 0:
            c.showPage()

        # Calculate position of current card on page
        card_index_on_page = i % cards_per_page
        x_pos = x_positions[card_index_on_page % 2]  # Left or right column
        y_pos = y_positions[card_index_on_page // 2]  # Top or bottom row

        # Load the SVG as a drawing
        drawing = svg2rlg(svg_file)
        
        # Scale the drawing to fit within card dimensions
        scale_factor_width = card_width / drawing.width
        scale_factor_height = card_height / drawing.height
        drawing.scale(scale_factor_width, scale_factor_height)

        # Draw the SVG card on the canvas
        renderPDF.draw(drawing, c, x_pos, y_pos)

    print(f"PDF generated: {output_pdf}")
    c.save()

# Example usage:
# generate_pdf_from_svgs("admit_cards_vertical.pdf", ["card1.svg", "card2.svg", "card3.svg", "card4.svg"])

from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg

def generate_pdf_from_svgs(output_pdf, svg_files):
    c = canvas.Canvas(output_pdf, pagesize=(595.28, 841.89))  # A4 size in points (Portrait)
    width, height = 595.28, 841.89  # A4 dimensions
    gap = 2.83465  # 1 mm gap in points for borders

    # Calculate dimensions to fit 4 cards (2 rows x 2 columns) with gaps on A4
    card_width = (width - 3 * gap) / 2  # Two columns, gap on left, center, right
    card_height = (height - 3 * gap) / 2  # Two rows, gap on top, middle, bottom

    cards_per_page = 4  # 2 rows and 2 columns per page
    
    # Calculate x and y positions for the cards on A4 (portrait)
    x_positions = [gap, width / 2 + gap / 2]  # Two columns (left and right positions)
    y_positions = [height - gap - card_height, height / 2 - gap / 2 - card_height]  # Two rows (top and bottom)

    for i, svg_file in enumerate(svg_files):
        # Add a new page after every 4 cards
        if i % cards_per_page == 0 and i > 0:
            c.showPage()

        # Determine the position of the current card on the page (0-3 for 4 cards per page)
        card_index_on_page = i % cards_per_page
        x_pos = x_positions[card_index_on_page % 2]  # Column (left or right)
        y_pos = y_positions[card_index_on_page // 2]  # Row (top or bottom)

        # Load the SVG as a drawing
        drawing = svg2rlg(svg_file)
        
        # Scale the drawing to fit within the calculated card dimensions
        scale_factor_width = card_width / drawing.width
        scale_factor_height = card_height / drawing.height
        drawing.scale(scale_factor_width, scale_factor_height)

        # Draw the scaled SVG card on the canvas at the calculated position
        renderPDF.draw(drawing, c, x_pos, y_pos)

    print(f"PDF generated: {output_pdf}")
    c.save()

# Example usage:
# generate_pdf_from_svgs("admit_cards.pdf", ["card1.svg", "card2.svg", "card3.svg", "card4.svg"])

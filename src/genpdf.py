from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg

def generate_pdf_from_svgs(output_pdf, svg_files):
    c = canvas.Canvas(output_pdf, pagesize=(595.28, 841.89))  # A4 size in points
    width, height = 595.28, 841.89
    card_width, card_height = 70 * 2.83465, 148.5 * 2.83465  # mm to points
    cards_per_page = 6
    x_positions = [10, width/2]  # Left and right
    y_positions = [10, height/3, 2*height/3]  # Three rows

    for i, svg_file in enumerate(svg_files):
        # Add a new page every 6 cards
        if i % cards_per_page == 0 and i > 0:
            c.showPage()

        # Calculate the position of the current card on the A4 layout
        card_index_on_page = i % cards_per_page
        x_pos = x_positions[card_index_on_page % 2]
        y_pos = y_positions[card_index_on_page // 2]

        # Load the SVG as a drawing
        drawing = svg2rlg(svg_file)
        renderPDF.draw(drawing, c, x_pos, y_pos)
    print(f"PDF generated: {output_pdf}")
    c.save()
    
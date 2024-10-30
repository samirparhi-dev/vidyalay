from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from datetime import datetime
import os

def generate_pdf_from_svgs(svg_files):
   
    # output_pdf_path_folder="/Users/samirparhi-dev/codeSpace/personal/vidyalay/test/admitCardA4/"
    output_pdf_path_folder="C:\\Users\\tknan\\Desktop\\tk\\\\admitCardA4\\"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_pdf_path = os.path.join(output_pdf_path_folder, f"{timestamp}_cards_output.pdf")
    c = canvas.Canvas(output_pdf_path, pagesize=(841.89, 595.28))
    width, height = 841.89, 595.28
    gap = 2.83465
    
    card_width = (width - 3 * gap) / 3  # 3 columns with gaps between and around
    card_height = (height - 3 * gap) / 2  # 2 rows with gaps between and around

    cards_per_page = 4  # 4 cards per page (3 columns x 2 rows)

    # Calculate x and y positions for the 3 columns and 2 rows
    x_positions = [gap, gap + card_width + gap]  # 2 columns
    y_positions = [height - gap - card_height, height - 2 * gap - 2 * card_height]  # 2 rows

    for i, svg_file in enumerate(svg_files):
        # Add a new page after every 6 cards
        if i % cards_per_page == 0 and i > 0:
            c.showPage()

        # Determine the position of the current card on the page
        card_index_on_page = i % cards_per_page
        x_pos = x_positions[card_index_on_page % 2]  # Column position
        y_pos = y_positions[card_index_on_page // 2]  # Row position

        # Load the SVG as a drawing
        drawing = svg2rlg(svg_file)
        
        # Scale the drawing to fit within card dimensions
        scale_factor_width = card_width / drawing.width
        scale_factor_height = card_height / drawing.height
        drawing.scale(scale_factor_width, scale_factor_height)

        # Draw the SVG card on the canvas
        renderPDF.draw(drawing, c, x_pos, y_pos)

    print(f"PDF generated: {output_pdf_path}")
    c.save()
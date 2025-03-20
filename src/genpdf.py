import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

# def fetch_image_from_url(image_url):
#     """
#     Fetch the image from the URL and return it as a BytesIO object.
#     """
#     try:
#         response = requests.get(image_url)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         return BytesIO(response.content)  # Return image content as a BytesIO object
#     except Exception as e:
#         print(f"Failed to fetch image: {e}")
#         return None

def generate_pdf_from_svgs(svg_files):
    output_pdf_path_folder = "C:\\Users\\tknan\\Desktop\\tk\\admitCardA4\\"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_pdf_path = os.path.join(output_pdf_path_folder, f"{timestamp}_cards_output.pdf")
    
    c = canvas.Canvas(output_pdf_path, pagesize=(841.89, 595.28))
    width, height = 841.89, 595.28
    gap = 2.83465
    
    card_width = (width - 3 * gap) / 2  # 2 columns with gaps between and around
    card_height = (height - 3 * gap) / 4 # 4 rows with gaps between and around

    cards_per_page = 8  # 8 cards per page (2 columns x 4 rows)

    # Calculate x and y positions for the 2 columns and 4 rows
    x_positions = [gap, gap + card_width + gap]  # 2 columns
    y_positions = [height - gap - card_height, height - 2 * gap - 2 * card_height]  # 4 rows

    for i, svg_file in enumerate(svg_files):
        # Add a new page after every 8 cards
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

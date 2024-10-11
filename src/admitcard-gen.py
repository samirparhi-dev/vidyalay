from jinja2 import Template
import math
import os
import cairosvg
from PyPDF2 import PdfMerger

# Define the card template (70mm x 148.5mm)
card_template = '''
<svg width="70mm" height="148.5mm" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="{{ background_color }}"/>
  <text x="50%" y="50%" font-size="6mm" fill="{{ text_color }}" text-anchor="middle" alignment-baseline="middle">{{ text }}</text>
</svg>
'''

# Define the A4 size SVG container template (210mm x 297mm) to hold 6 cards
a4_template = '''
<svg width="210mm" height="297mm" xmlns="http://www.w3.org/2000/svg">
  {% for card in cards %}
  <g transform="translate({{ card.x }}mm, {{ card.y }}mm)">
    {{ card.svg }}
  </g>
  {% endfor %}
</svg>
'''

# Create a Jinja2 template for the cards
card_template = Template(card_template)

# Function to create card data with text
def create_card_data(card_number, background_color, text_color):
    text = f'Card {card_number}'
    return card_template.render(
        background_color=background_color,
        text_color=text_color,
        text=text
    )

# Create a Jinja2 template for the A4 page
a4_template = Template(a4_template)

# Fixed background and text colors for all cards
background_color = '#FFCCCC'  # Light red background
text_color = '#000000'  # Black text

# Directory to store the intermediate SVG and PDF files
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

cards_per_page = 6
total_cards = 160
num_pages = math.ceil(total_cards / cards_per_page)

# List to keep track of the generated PDF files
pdf_files = []

for page in range(num_pages):
    card_svgs = []
    
    for card_index in range(cards_per_page):
        card_number = page * cards_per_page + card_index + 1
        if card_number > total_cards:
            break  # stop if all cards are processed

        card_svg = create_card_data(card_number, background_color, text_color)

        # Calculate position of the card on the page
        x_pos = (card_index % 3) * 70  # 3 columns
        y_pos = (card_index // 3) * 148.5  # 2 rows

        card_svgs.append({
            'x': x_pos,
            'y': y_pos,
            'svg': card_svg
        })

    # Render the A4 layout with 6 cards
    rendered_a4_svg = a4_template.render(cards=card_svgs)

    # Save the rendered SVG to a file
    svg_filename = os.path.join(output_dir, f'a4_page_{page + 1}.svg')
    with open(svg_filename, 'w') as f:
        f.write(rendered_a4_svg)

    # Convert the SVG to a PDF
    pdf_filename = os.path.join(output_dir, f'a4_page_{page + 1}.pdf')
    cairosvg.svg2pdf(url=svg_filename, write_to=pdf_filename)
    
    # Keep track of the generated PDF file
    pdf_files.append(pdf_filename)
    
    print(f"Page {page + 1} rendered and saved as '{pdf_filename}'.")

# Merge all PDF files into a single multi-page PDF
merged_pdf_filename = os.path.join(output_dir, 'cards_merged.pdf')
merger = PdfMerger()

for pdf_file in pdf_files:
    merger.append(pdf_file)

merger.write(merged_pdf_filename)
merger.close()

print(f"All pages merged into '{merged_pdf_filename}'.")
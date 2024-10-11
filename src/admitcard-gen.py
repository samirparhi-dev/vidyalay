from jinja2 import Template
import os
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas

# Import the function from utils.py
from utils import create_card, read_data_from_csv, get_svg_template
from genpdf import generate_pdf_from_svgs

# Function to save rendered SVG to a file
def save_svg(content, output_file):
    with open(output_file, 'w') as f:
        f.write(content)


# Main Function
if __name__ == "__main__":
    # Paths
    csv_file_path = input('Where is your Csv file?')
    if not csv_file_path:
        csv_file_path = "default.csv"
    print(f"CSV file path: {csv_file_path}")

    output_pdf_path =  input('Where you want to save output file?')
    if not output_pdf_path:
        output_pdf_path = "default.pdf"
        print(f"Output PDF path: {output_pdf_path}")

    admit_card_svg_template = get_svg_template()
    
    # A4 size SVG 
    a4_svg_template = get_svg_template("/template/a4-design.svg")

    #Csv file read    
    data = read_data_from_csv(csv_file_path)

    # Create individual SVG cards
    svg_files = []

    for i, row in enumerate(data):
        card_svg = create_card(
                        row['Student Name'],
                        row['Class'],
                        row['Roll No'],
                        row['Centre Name'],
                        row['School Name'],
                        row['Gender'],
                        row['Exam Start Time'],
                        row['Exam End Time'],
                        a4_svg_template
                    )

        output_svg_file = f'card_{i}.svg'
        save_svg(card_svg, output_svg_file)
        svg_files.append(output_svg_file)

    # Generate the PDF from the SVG files
    generate_pdf_from_svgs(output_pdf_path, svg_files)

    
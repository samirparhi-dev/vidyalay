from jinja2 import Template
import os
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from datetime import datetime

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
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ###For Windows#####
    
    admit_card_path = "C:\\Users\\tknan\\Desktop\\tk\\admitCard\\"
    admit_card_svg_template = get_svg_template("C:\\Users\\tknan\\Code\\vidyalay\\template\\admit-card-design.svg")
    csv_file_path = "C:\\Users\\tknan\\Desktop\\tk\\SCPUR.csv"
    
    
    ######For MacOS#####
    
    # admit_card_path = "/Users/samirparhi-dev/codeSpace/personal/vidyalay/test/admitCard"
    # admit_card_svg_template = get_svg_template("/Users/samirparhi-dev/codeSpace/personal/vidyalay/template/admit-card-design.svg")
    # csv_file_path = "/Users/samirparhi-dev/codeSpace/personal/vidyalay/default.csv"
    
    if not csv_file_path:
        print(f"CSV file path: {csv_file_path}")
    output_pdf_path =  input('Where you want to save output file?')
    if not output_pdf_path:
        print(f"Output PDF path: {output_pdf_path}")
    #Csv file read    
    data = read_data_from_csv(csv_file_path)

    # Create individual SVG cards
    svg_files = []

    for i, row in enumerate(data):
        # print(row)
        # print(row.keys())
        card_svg = create_card(
                        
                        row['Class'],
                        row['Student Name'],
                        row['Roll No'],
                        row['Centre Name'],
                        row['School Name'],
                        row['Gender'],
                        row['Exam Start Time'],
                        row['Exam End Time'],
                        row['Date'],
                        row['Caste'],
                        admit_card_svg_template
                    )
        student_name = "".join(c for c in row['Student Name'] if c.isalnum() or c in (' ', '-', '_')).replace(" ", "_")

        # Save SVG to file
        output_svg_file = os.path.join(admit_card_path, f'{student_name}_Admit_card.svg')
        # Save the SVG file
        save_svg(card_svg, output_svg_file)
    
        # Append the SVG file path to the list
        svg_files.append(output_svg_file)

    # Generate the PDF from the SVG files
    generate_pdf_from_svgs(svg_files)
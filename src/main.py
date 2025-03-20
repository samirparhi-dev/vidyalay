from jinja2 import Template
import os
from datetime import datetime

# Import the function from utils.py
from utils import create_card, read_data_from_csv, get_svg_template, fetch_image_from_url
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
    
    admit_card_path = "C:\\Users\\tknan\\Desktop\\tk\\admitCard\\"
    admit_card_svg_template = get_svg_template("C:\\Users\\tknan\\Code\\vidyalay\\template\\admit-card-design.svg")
    csv_file_path = "C:\\Users\\tknan\\Desktop\\tk\\tapas.csv"
    
    output_pdf_path = input('Where you want to save output file?')

    # Csv file read    
    data = read_data_from_csv(csv_file_path)

    # Create individual SVG cards
    svg_files = []

    for i, row in enumerate(data):
        print(row['photo of the student'])
        # Fetch the image from URL and get it as a BytesIO object
        image_data = fetch_image_from_url(row['photo of the student'])
        
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
            image_data,  # Pass the image data
            admit_card_svg_template
        )
        
        student_name = "".join(c for c in row['Student Name'] if c.isalnum() or c in (' ', '-', '_')).replace(" ", "_")

        # Save SVG to file
        output_svg_file = os.path.join(admit_card_path, f'{student_name}_Admit_card.svg')
        save_svg(card_svg, output_svg_file)
    
        # Append the SVG file path to the list
        svg_files.append(output_svg_file)

    # Generate the PDF from the SVG files
    generate_pdf_from_svgs(svg_files)
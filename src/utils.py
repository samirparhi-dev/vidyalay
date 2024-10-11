from jinja2 import Template
import csv
import os
# Function to generate SVG card with dynamic data
def create_card(class_name, student_name, student_roll_no, exam_centre_name, school_name, student_gender, exam_start_time, exam_end_time, svg_template):
    return svg_template.render(
        studentClass=class_name,
        studentName=student_name,
        studentRoll_no=student_roll_no,
        studentCentre_name=exam_centre_name,
        studentSchool_name=school_name,
        studentGender=student_gender,
        examStartTime=exam_start_time,
        examEndTime=exam_end_time
    )
def read_data_from_csv(csv_file_path):
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def get_svg_template(default_path="/template/admit-card-design.svg"):
    # Ask the user for the SVG file path
    svg_file_path = input('Please provide the SVG file path: ')
    
    # Use the default path if no input is provided
    if not svg_file_path:
        svg_file_path = default_path
        print(f"No path provided. Using default SVG file: {svg_file_path}")
    
    # Check if the file exists
    if not os.path.exists(svg_file_path):
        print(f"Error: File '{svg_file_path}' not found. Please provide a valid file path.")
        return None
    else:
        # Load and return the SVG template
        return Template(load_svg(svg_file_path))
def load_svg(file_path):
    with open(file_path, 'r') as file:
        svg_content = file.read() 
    return svg_content
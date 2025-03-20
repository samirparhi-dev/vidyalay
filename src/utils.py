import os
import pandas as pd
from io import BytesIO
from jinja2 import Template
import requests
import base64

# Function to generate SVG card with dynamic data
def create_card(class_name, student_name, student_roll_no, exam_centre_name, school_name, student_gender, exam_start_time, exam_end_time, exam_date, student_caste, image_data, svg_template):
    # If the image is a URL, convert it to base64
    if image_data:
        image_base64 = image_to_base64(image_data)
    else:
        image_base64 = None
    
    return svg_template.render(
        studentClass=class_name,
        studentName=student_name,
        studentRoll_no=student_roll_no,
        parent=parent,
        studentSchool_name=school_name,
        ContactNo=ContactNo,
        
        
        img=image_base64
    )

def image_to_base64(image_data):
    """Convert image data to base64 encoding."""
    image_data.seek(0)  # Ensure we're at the start of the BytesIO object
    return base64.b64encode(image_data.read()).decode('utf-8')

def read_data_from_csv(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df.to_dict('records')

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

def fetch_image_from_url(image_url):
    """Fetch the image from the URL and return it as a BytesIO object."""
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return BytesIO(response.content)  # Return image content as a BytesIO object
    except Exception as e:
        print(f"Failed to fetch image: {e}")
        return None

def load_svg(file_path):
    """Load SVG template from file."""
    with open(file_path, 'r') as file:
        svg_content = file.read() 
    return svg_content

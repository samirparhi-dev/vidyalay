import csv
import sys
# Check if the CSV file path is provided as an argument
if len(sys.argv) < 2:
    print("Error: CSV file path not provided.")
    sys.exit(1)

csv_file_path = sys.argv[1]

input_file = csv_file_path
static_first_text = """
<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Four Rectangular Boxes</title>
    <style>
    .container {
        width: 21cm; /* A4 width */
        display: flex;
        flex-wrap: wrap;
    }
    .box {
        width: 4in;
        height: 6in;
        border: 2px solid #000;
        overflow: hidden;
    }
    .rotated-text {
        transform: rotate(90deg); /* Rotate text by 90 degrees */
        white-space:wrap; /* Prevent text from wrapping */
        overflow: hidden; /* Prevent overflow */
        text-overflow: ellipsis; /* Add ellipsis if text overflows */
        margin: 10; /* Reset default margin */
    }
    </style>
    </head>
    <body>
    <div class="container">"""
static_end_text = """  
            </div>
            </body>
            </html>
            """
# Open CSV file
with open(input_file, 'r') as file:
    reader = csv.DictReader(file)

    # Loop through each row in the CSV
    for row in reader:
        # Extracting only the required columns
        school_name = row.get('School Name', '')
        student_name = row.get('Student Name', '')
        dob = row.get('Date of Birth', '')
        student_class = row.get('Student Class', '')
        year = row.get('year', '')
        gender = row.get('gender', '')
        centre_name = row.get('Centre Name', '')
        roll_no = row.get('Roll No', '')
        examination_date = row.get('Examination Date', '')
        exam_start_time = row.get('Exam Start Time', '')
        exam_end_time = row.get('Exam End Time', '')
        
        custom_paragraph =""
        custom_paragraph += """<div class="box"><h2><center>Admit Card</center></h2><br><h3><center>Block Education office Udala</center></h3><br><p><center>form no -04</center></p><br><p> Upper Primary class {student_class}<br>Scholarship Examination {year}</p><br><p> Scholarship Examination {year}<br>Name of the Student: {gender} {student_name}<br>School Name: {school_name}<br>Centre Name: {centre_name}<br>Roll No: {roll_no}<br>Examination Date: {roll_no}<br>Examination Time: {exam_start_time} to {exam_end_time}<br><br><br>Student Signature<br>Block Education officer Signature<br> Headmaster or Headmistress</p></div>"""

final_string = static_first_text + custom_paragraph + static_end_text

file_path = "admitcard.html"
with open(file_path, "w") as file:
    file.write(final_string)
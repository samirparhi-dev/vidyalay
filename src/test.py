from fpdf import FPDF
import pandas as pd

# Define constants for layout
A4_WIDTH, A4_HEIGHT = 210, 297  # A4 dimensions in mm
CARD_WIDTH, CARD_HEIGHT = 90, 60  # Standard ID card size in mm
MARGIN_X, MARGIN_Y = 6, 6  # Margins around cards
CARDS_PER_ROW = 2
CARDS_PER_COLUMN = 4
CARDS_PER_PAGE = CARDS_PER_ROW * CARDS_PER_COLUMN
SPACING_X = (A4_WIDTH - (CARDS_PER_ROW * CARD_WIDTH) - (2 * MARGIN_X)) / (CARDS_PER_ROW - 1)
SPACING_Y = (A4_HEIGHT - (CARDS_PER_COLUMN * CARD_HEIGHT) - (2 * MARGIN_Y)) / (CARDS_PER_COLUMN - 1)

# Load the CSV file
file_path = "/Users/samirparhi-dev/codeSpace/personal/vidyalay/BLOCK LEVEL EXCURSION TRIP DATA.csv"
df = pd.read_csv(file_path)

# Initialize PDF
pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.set_auto_page_break(auto=True, margin=10)
pdf.set_font("Arial", size=8)


# Function to add an ID card
def add_id_card(pdf, x, y, student):
    pdf.set_xy(x, y)
    pdf.rect(x, y, CARD_WIDTH, CARD_HEIGHT, style="D")  # Draw ID card border

    # Add Heading (Centered) with underline effect
    pdf.set_xy(x, y + 3)
    pdf.set_font("Arial", style="B", size=10)
    heading_text = "Block Education Office, Udala"
    pdf.cell(CARD_WIDTH, 5, heading_text, align="C", ln=True)

    # Underline the heading by drawing a line below it
    heading_width = pdf.get_string_width(heading_text)  # Get the width of the text
    underline_y_position = y + 3 + 5  # Y position of the underline (below the text)
    pdf.line(
        x + (CARD_WIDTH - heading_width) / 2,  # Start X position (centered)
        underline_y_position,
        x + (CARD_WIDTH - heading_width) / 2 + heading_width,  # End X position
        underline_y_position
    )

    # Add text
    pdf.set_xy(x + 7, y + 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(CARD_WIDTH - 10, 5,
                   f"Name: {student['NAME OF THE STUDENT']}\n"
                   f"Class: {student['CLASS']}\n"
                   f"Gender: {student['GENDER']}\n"
                   f"Father: {student['NAME OF THE FATHER']}\n"
                   f"School: {student['NAME OF THE SCHOOL']}\n"
                   f"Cluster: {student['NAME OF THE CLUSTER']}\n"
                   f"Contact: {student['CONTACT NUMBER']}\n"
                   f"Emergency contact: 8917642575, 8249231018")


# Generate pages with ID cards
for i, student in df.iterrows():
    if i % CARDS_PER_PAGE == 0:
        pdf.add_page()

    row = (i % CARDS_PER_PAGE) // CARDS_PER_ROW
    col = (i % CARDS_PER_PAGE) % CARDS_PER_ROW

    x = MARGIN_X + col * (CARD_WIDTH + SPACING_X)
    y = MARGIN_Y + row * (CARD_HEIGHT + SPACING_Y)
    add_id_card(pdf, x, y, student)

# Save PDF
pdf_output_path = "/Users/samirparhi-dev/codeSpace/personal/vidyalay/Identity_Cards.pdf"
pdf.output(pdf_output_path)

# Return the file path
pdf_output_path

extern crate csv;
extern crate pdf_diploma;

use csv::ReaderBuilder;
use pdf_diploma::{Diploma, Element, Position, TextElement};

fn create_admit_card(name: &str, dob: &str, school_name: &str, canvas: &mut Diploma) {
    let styles = canvas.create_style()
        .font_size(16.0)
        .font_name("Helvetica-Bold")
        .build()
        .unwrap();

    let body_style = canvas.create_style()
        .font_size(12.0)
        .font_name("Helvetica")
        .build()
        .unwrap();

    canvas.add_element(
        Element::Text(TextElement::new(school_name.to_owned(), styles)),
        Position::new(50.0, 700.0), // Adjust coordinates as needed
    );

    canvas.add_element(
        Element::Text(TextElement::new("Admit Card".to_owned(), styles)),
        Position::new(50.0, 650.0), // Adjust coordinates as needed
    );

    canvas.add_element(
        Element::Text(TextElement::new("Name:".to_owned(), body_style)),
        Position::new(50.0, 600.0), // Adjust coordinates as needed
    );

    canvas.add_element(
        Element::Text(TextElement::new(name.to_owned(), body_style)),
        Position::new(100.0, 600.0), // Adjust coordinates as needed
    );

    canvas.add_element(
        Element::Text(TextElement::new("Date of Birth:".to_owned(), body_style)),
        Position::new(50.0, 550.0), // Adjust coordinates as needed
    );

    canvas.add_element(
        Element::Text(TextElement::new(dob.to_owned(), body_style)),
        Position::new(150.0, 550.0), // Adjust coordinates as needed
    );
}

fn create_admit_cards(data: Vec<csv::Record>, filename: &str) -> Result<(), std::io::Error> {
    let mut diploma = Diploma::new("A4".to_owned())?; // Set page size as A4

    // Adjust margins and spacing as needed
    let margin = 50.0;
    let spacing = 20.0;
    let card_width = diploma.get_width() / 2.0 - margin - spacing;
    let card_height = diploma.get_height() / 2.0 - margin - spacing;

    let mut row = 0;
    let mut col = 0;

    for record in data.iter() {
        let name = record.get(0).unwrap().to_string();
        let dob = record.get(1).unwrap().to_string();
        let school_name = record.get(2).unwrap().to_string();

        let x = margin + col * (card_width + spacing);
        let y = diploma.get_height() - margin - row * (card_height + spacing);

        create_admit_card(&name, &dob, &school_name, &mut diploma);

        col += 1;
        if col == 2 {
            col = 0;
            row += 1;
        }

        if row == 2 {
            diploma.write(filename)?; // Save after every 2 cards
            diploma = Diploma::new("A4".to_owned())?; // Create new diploma for next page
            row = 0;
        }
    }

    diploma.write(filename)?; // Save the remaining cards
    Ok(())
}

fn main() -> Result<(), std::io::Error> {
    let mut csv_reader = ReaderBuilder::new()
        .from_path("students.csv")? // Replace with your CSV path
        .has_headers(true) // Assuming headers are present
        .build();

    let mut data = Vec::new();
    for record in csv_reader.records() {
        data.push(

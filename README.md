# Contact-Book

A simple command-line Contact Book application built with Python. It allows users to manage their contacts by adding, viewing, searching, editing, and deleting contact information.

## Features

- **Add Contact:** Save a contact's name, phone number, and email address.
- **View Contacts:** Display all saved contacts alongside their unique IDs.
- **Search Contacts:** Find contacts by name.
- **Edit Contact:** Update a contact's name, phone number, or email address using its unique ID.
- **Input Validation:** Validate user inputs to prevent empty names, invalid phone numbers, and incorrectly formatted email addresses.
- **Duplicate Prevention:** Prevent multiple contacts from having the same phone number or email address.
- **Unique Contact IDs:** Automatically generate a unique ID for every contact, allowing multiple contacts to have the same name.

## Technologies Used

- Python 3

## Getting Started

### Prerequisites

You need Python 3 installed on your computer.

### Installation

1. Clone the repository:

   ```bash
   git clone <https://github.com/Coal77/contact-book.git>
   ```

2. Navigate to the project directory:

   ```bash
   cd contact-book
   ```

3. Run the application:

   ```bash
   python contact-book.py
   ```

## How to Use

After running the application, a menu will appear with the following options:

1. Add a contact
2. View Contact Book
3. Search for a contact
4. Edit Contact
5. Delete Contact
6. Exit

Enter the corresponding number to perform an operation.

## Current Limitations

- Contacts are stored in memory using a Python dictionary. They are not saved permanently, so all contacts are lost when the application is closed.
- Contact searches are performed using names. If multiple contacts share the same name, all matching contacts are displayed.

## Future Improvements

- Implement permanent storage so contacts remain available after closing the application.
- Improve contact search and management options.
- Add more robust email and phone number validation.
- Implement the delete contact functionality.
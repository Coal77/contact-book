import sys

contact_book = {}

def menu() :
    print(
        "\n=====Contact Book=====\n"
        "Enter a number to choose operation\n"
        "1. Add a contact\n"
        "2. View Contact Book\n"
        "3. Search for a contact\n"
        "4. Edit Contact\n"
        "5. Delete Contact\n"
        "6. Exit\n"
    )

def sanitize_name(user_in: str) :
    user_input = user_in.strip()
    if not user_input :
        return None, ValueError("Input cannot be empty!")
    
    return user_input.title(), None

def sanitize_digit(user_in: str) :
    user_input = user_in.strip()
    if not user_input :
        return None, "Phone number cannot be empty!"
    
    if not user_input.isdigit() :
        return None, "Phone number can only contain numbers!"
    
    return user_input, None

def sanitize_email(user_in: str) :
    cleaned = user_in.strip().lower()

    #* This allows for email to be optional
    if not cleaned :
        return None, None
    
    if cleaned.count("@") != 1 :
        return None, "Invalid email format! Example: name@domain.com"
    
    name, domain = cleaned.split("@")
    
    if not name or not domain :
        return None, "Invalid email format! Example: name@domain.com"
    
    if "." not in domain :
        return None, "Invalid email format! Example: name@domain.com"
    
    if domain.startswith(".") or domain.endswith(".") :
        return None, "Invalid email format! Example: name@domain.com"
    
    if ".." in cleaned :
        return None, "Invalid email format! Example: name@domain.com"
    
    return cleaned, None

def get_valid_input(prompt: str, validate_fn, allow_empty = False) -> str :
    while True :
        user_input = input(prompt)
        
        if allow_empty and not user_input.strip() :
            return None
        
        value, err = validate_fn(user_input)

        if err is None :
            return value
        
        print(f"Error! {err}\n")

def generate_id(container: dict) -> str:
    if not container:
        return "001"
    highest = max(int(contact_id[1:]) for contact_id in container)
    return f"{highest + 1:03d}"

def add_contact(container: dict, cntct_name: str, cntct_no: str, cntct_email = None) :
    #* Handle duplicate contact information 
    for details in container.values() :
        if details["phone"] == cntct_no :
            return None, "This phone number is already saved!"
        
        if cntct_email is not None and details["email"] == cntct_email :
            return None, "This email address is already saved!"

    #* Generate id after validation pass
    id = generate_id(container)

    container[id] = {
        "name": cntct_name,
        "phone": cntct_no,
        "email": cntct_email
    }

    return "Contact added successfully", None

def view_contacts(container: dict) -> tuple[str | None, str | None] :
    if not container :
        return None, "There are no saved contacts!"
    
    items = []
    for contact_id, v in container.items() :
        lines = [f"[{contact_id}]: {v["name"]}", f"Phone: {v['phone']}"]
        if v["email"] is not None:
            lines.append(f"Email: {v["email"]}")

        items.append("\n".join(lines))
        
    return "\n\n".join(items), None

def search_contacts(container: dict, cntct_name: str) -> str :
    if not container :
        return None, "There are no saved contacts!"

    cleaned = cntct_name.title()
    matches = []
    for key in container.keys():
        if container[key]["name"] == cleaned:
            phone = container[key]["phone"]
            email = container[key]["email"] or "no email available"
            contact_string = f"{cleaned} : {phone}, {email}"
            matches.append(contact_string)

    if not matches:
        return None, "Contact not found"

    return "\n".join(matches), None

def edit_contacts(container: dict, old_name: str, new_name: str, new_phone, new_email) :
    #* Check if there are no saved contacts in the contact book
    if not container :
        return None, "There are no contacts to edit!"
    
    """
        {
            "Faith_000": {"phone": 000, "email": ""}
        }
    """

    #* Check if old name has not been saved previously
    if old_name not in container :
        return None, "Contacts not found!"
    
    if new_name is not None and new_name != old_name :
        if new_name in container :
            return None, "You have a contact with this name!"
        
        container[new_name] = container.pop(old_name)
        target_key = new_name
    else :
        target_key = old_name

    if new_phone is not None:
        container[target_key]["phone"] = new_phone
    
    if new_email is not None:
        container[target_key]["email"] = new_email

    return container, None
    

while True :
    menu()
    user_input = input("Enter a number to choose operation: ")

    if user_input == "1" :
        contact_name = get_valid_input("Enter Contact name: ", sanitize_name)
        contact_no = get_valid_input("Enter Contact No: ", sanitize_digit)
        contact_email = get_valid_input("Enter Contact email: ", sanitize_email)

        contact, err = add_contact(contact_book, contact_name, contact_no, contact_email)

        if err is not None :
            print(f"Error! {err}")
        else :
            print("Contact added successfully!")

    elif user_input == "2" :
        print("===Contacts===")

        contacts, err = view_contacts(contact_book)

        if err:
            print(err)
        else :
            print(contacts)

    elif user_input == "3" :
        contact_search = get_valid_input("Enter contact name to search: ", sanitize_name)

        contact, err = search_contacts(contact_book, contact_search)
        if err is not None :
            print(f"\nError! {err}")
        else :
            print(contact)
    
    elif user_input == "4" :

        old_name = get_valid_input("Enter contact name to edit contact info: ", sanitize_name)
        new_name = get_valid_input("Enter new name: ", sanitize_name, allow_empty=True)
        new_phone = get_valid_input("Enter new phone: ", sanitize_digit, allow_empty=True)
        new_email = get_valid_input("Enter new email information: ", sanitize_email)

        new_name = new_name or None

        contact, err = edit_contacts(contact_book, old_name, new_name, new_phone, new_email)

        if err is not None :
            print(f"Error! {err}")

    elif user_input == "6":
        print("Thank you for using our Service")
        sys.exit()


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

def search_by_name(container: dict, name: str) -> tuple[dict | None, str | None]:
    target = name.strip().title()
    results = {}

    for contact_id, dict_val in container.items():
        if dict_val["name"] == target:
            results[contact_id] = dict_val

    if not results:
        return None, f"There are no contacts found with the name '{target}'"

    return results, None

def is_duplicate(container: dict, field: str, value: str, ignore_id: str = None):
    for contact_id, details in container.items():
        if contact_id == ignore_id:
            continue

        if details[field] == value:
            return True

    return False

def generate_id(container: dict) -> str:
    if not container:
        return "001"
    highest = max(int(contact_id) for contact_id in container)
    return f"{highest + 1:03d}"

def add_contact(container: dict, cntct_name: str, cntct_no: str, cntct_email = None) :
    #* Handle duplicate contact information 
    if cntct_no is not None and is_duplicate(container, "phone", cntct_no):
        return None, "This phone number is already saved!"
    
    if cntct_email is not None and is_duplicate(container, "email", cntct_email) :
        return None, "This email address is already saved!"

    #* Generate id after validation pass
    contact_id = generate_id(container)

    container[contact_id] = {
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

def edit_contacts(container: dict, contact_id: str, new_name: str,new_phone: str, new_email: str) -> tuple[str | None, str | None]:
    if not container:
        return None, "There are no saved contacts to edit"

    #todo Check if it is needed to use a while loop
    #todo Check about creating a function for different messages
    if contact_id not in container:
        return None, ValueError("Contact not found!")
    
    #todo Check if it is better to use get valid input to get the new names when appropiate
    """
        001: {
            "name": Faith,
            "phone": 081,
            'email": faith@gmail.com
        }
    """

    #* Check if user inputs a field and if it's not a duplicate. Name shouldn't be checked cause multiple names are allowed
    if new_phone is not None and is_duplicate(container, "phone", new_phone, contact_id):
        return None, "Another contact has this number!"
    
    if new_email is not None and is_duplicate(container, "email", new_email, contact_id):
        return None, "Another contact has this email!"

    if new_name is not None:
        container[contact_id]["name"] = new_name

    if new_phone is not None:
        container[contact_id]["phone"] = new_phone

    if new_email is not None:
        container[contact_id]["email"] = new_email

    
    return container, None

while True :
    menu()
    user_input = get_valid_input("Enter a number to choose operation: ", sanitize_digit)

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
        old_name = get_valid_input("Enter contact name to edit: ", sanitize_name, allow_empty=False)
        
        #* Search contacts by name to allow users select by id
        matches, err = search_by_name(contact_book, old_name)
        if err is not None :
            print(f"Error! {err}")
            continue
        else:
            contacts, err = view_contacts(matches)
            if err:
                print(f"Error! {err}")
            else:
                print(contacts)

        contact_id = get_valid_input("Select contact-id to edit contact's details: ", sanitize_digit)

        new_name = get_valid_input("Enter new name: ", sanitize_name, allow_empty=True)

        while True:
            new_phone = get_valid_input("Enter new phone number: ", sanitize_digit, allow_empty=True)

            if new_phone and is_duplicate(contact_book, "phone", new_phone, contact_id):
                print("Error! This number is already saved!")
                continue

            break


        while True:
            new_email = get_valid_input("Enter new email: ", sanitize_email)

            if new_email and is_duplicate(contact_book, "email", new_email, contact_id):
                print("Error! This email is already saved!")
                continue

            break

        result, err = edit_contacts(contact_book, contact_id, new_name, new_phone, new_email)

        if err is not None :
            print(f"Error! {err}")
        else:
            contact, _ = view_contacts(contact_book)
            print(contact)

    elif user_input == "6":
        print("Thank you for using our Service")
        sys.exit()


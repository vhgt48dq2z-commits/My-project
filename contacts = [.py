contacts = [
    {'name': 'Geektech', 'phone': '0507052018'},
    {'name': 'Служба спасения', 'phone': '911'},
    {'name': 'Пожарная служба', 'phone': '101'},
]
print(contacts)
def create_contact(items):
    input_name = input("Enter name: ")
    input_phone = input("Enter phone: ")
    new_info = {'name': input_name, 'phone':input_phone}
    items.append(new_info)
    print(items)

print(contacts)

def editcontact(items):
    input_name = input("Enter name to edit: ").lower().strip()
    for contact in items:
        if contact['name'].lower().strip() == input_name:
            new_name = input("Enter new name or press Enter to keep the same: ")
            new_phone = input("Enter new phone or press Enter to keep the same: ")
            if new_name:
                contact['name'] = new_name
            if new_phone:
                contact['phone'] = new_phone
            print(f"Updated contact: {contact}")
            break
    else:
        print("Contact not found.")

def delete_contact(items):
    input_name = input("Enter name to delete: ")
    for contact in items:
        if contact['name'].lower().strip() == input_name.lower().strip():
            items.remove(contact)
            print('Contact deleted.')
            break
    else:
        print("Contact not found")
    







while True:
    print("What do you want to do? ")
    print("1.Create new contact")
    print("2.edit contact")
    print("3.delete contact")
    print("4.show all contacts")
    print("5.exit")
    answer = input("").strip()
    if answer == '1':
        create_contact(contacts)
    elif answer == '2':
        editcontact(contacts)
    elif answer == '3':
        delete_contact(contacts)
    elif answer == '4':
        print(contacts)
    elif answer == '5':
        break
    else:
        print("Invalid option. Please try again.")
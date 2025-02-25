import os
import pickle

# load registered personage
def load_registered_faces(file_path='registered_faces.pkl'):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return {}

# save registered personage
def save_registered_faces(face_data, file_path='registered_faces.pkl'):
    with open(file_path, 'wb') as f:
        pickle.dump(face_data, f)

# list saved registered personage
def display_registered_employees(registered_faces):
    if registered_faces:
        print("Registered Employees:")
        for i, employee_name in enumerate(registered_faces, 1):
            print(f"{i}. {employee_name}")
    else:
        print("No registered employees.")

# delete certain personage
def delete_employee(registered_faces):
    display_registered_employees(registered_faces)
    employee_name = input("Enter the name of the employee to delete: ")
    if employee_name in registered_faces:
        del registered_faces[employee_name]
        save_registered_faces(registered_faces)
        print(f"Employee {employee_name} has been deleted.")
    else:
        print(f"Employee {employee_name} not found.")

# edit peronage information
def edit_employee(registered_faces):
    display_registered_employees(registered_faces)
    old_name = input("Enter the name of the employee to edit: ")
    if old_name in registered_faces:
        new_name = input("Enter the new name for the employee: ")
        registered_faces[new_name] = registered_faces.pop(old_name)
        save_registered_faces(registered_faces)
        print(f"Employee {old_name} has been updated to {new_name}.")
    else:
        print(f"Employee {old_name} not found.")

# main loop
if __name__ == "__main__":
    registered_faces = load_registered_faces()
    while True:
        print("\nOptions:")
        print("1. Display registered employees")
        print("2. Delete an employee")
        print("3. Edit an employee's name")
        print("4. Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            display_registered_employees(registered_faces)
        elif choice == '2':
            delete_employee(registered_faces)
        elif choice == '3':
            edit_employee(registered_faces)
        elif choice == '4':
            break
        else:
            print("Invalid option. Please try again.")

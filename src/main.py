from src.config.db_config import init_db
from src.services.db_services import UserService


def main():
    init_db()

    user_service = UserService()

    print("\n=== User Management System ===\n")

    while True:
        print("\n1. Create user")
        print("2. Read all users")
        print("3. Read user by ID")
        print("4. Update user")
        print("5. Delete user")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ")

        match choice:
            case '1':
                try:
                    name = input("Enter name: ")
                    email = input("Enter email: ")
                    age = int(input("Enter age: "))
                    user_id = user_service.create_user(name, email, age)
                    print(f"User created with ID: {user_id}")
                except ValueError as e:
                    print(f"Error: {e}")

            case '2':
                users = user_service.get_all_users()
                print("\nAll users:")
                if users:
                    for user in users:
                        print(
                            f"ID: {user.id}, Name: {user.name}, Email: {user.email}, Age: {user.age}")
                else:
                    print("No users found")

            case '3':
                try:
                    user_id = int(input("Enter user ID: "))
                    user = user_service.get_user_by_id(user_id)
                    if user:
                        print(f"\nID: {user.id}")
                        print(f"Name: {user.name}")
                        print(f"Email: {user.email}")
                        print(f"Age: {user.age}")
                    else:
                        print(f"No user found with ID {user_id}")
                except ValueError:
                    print("Please enter a valid ID")

            case '4':
                try:
                    user_id = int(input("Enter user ID to update: "))
                    user = user_service.get_user_by_id(user_id)
                    if user:
                        print(f"Current user: {user}")
                        name = input(f"Enter new name ({user.name}): ") or None
                        email = input(
                            f"Enter new email ({user.email}): ") or None
                        age_input = input(f"Enter new age ({user.age}): ")
                        age = int(age_input) if age_input else None

                        if user_service.update_user(user_id, name, email, age):
                            print("User updated successfully")
                    else:
                        print(f"No user found with ID {user_id}")
                except ValueError as e:
                    print(f"Error: {e}")

            case '5':
                try:
                    user_id = int(input("Enter user ID to delete: "))
                    if user_service.delete_user(user_id):
                        print("User deleted successfully")
                    else:
                        print(f"No user found with ID {user_id}")
                except ValueError:
                    print("Please enter a valid ID")

            case '6':
                break

            case _:
                print("Invalid choice. Please try again.")

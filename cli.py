import sys
from service_layer.unit_of_work import JsonUnitOfWork
from service_layer.service import FolderService
from models import Folder, File

# Initialize JSON database and repository
folder_service = FolderService(JsonUnitOfWork())

def print_menu():
    print("\n")
    print("Select an option:")
    print("1. Create a new folder")
    print("2. Add a file to a folder")
    print("3. Move a folder to another folder")
    print("4. Delete a file from a folder")
    print("5. Delete a folder and all its files")
    print("6. List all files in a folder")
    print("7. Exit")
    print("\n")

def create_folder():
    folder_name = input("Enter the folder name: ")
    parent_id = input("Enter the parent folder ID (leave blank for root): ") or None
    folder_id = folder_service.create_folder(folder_name, parent_id)
    print(f"Folder '{folder_name}' created with ID: {folder_id}")

def add_file_to_folder():
    folder_id = input("Enter the folder ID to add a file: ")
    file_name = input("Enter the file name: ")
    file_url = input("Enter the file URL: ")
    file = File(file_name=file_name, upload_url=file_url)
    folder_service.add_file_to_folder(folder_id, file)
    print(f"File '{file_name}' added to folder ID: {folder_id}")

def move_folder():
    folder_id = input("Enter the folder ID to move: ")
    target_folder_id = input("Enter the target folder ID: ")
    folder_service.move_folder(folder_id, target_folder_id)
    print(f"Folder ID {folder_id} moved to Folder ID {target_folder_id}")

def delete_file_from_folder():
    folder_id = input("Enter the folder ID: ")
    file_name = input("Enter the file name to delete: ")
    folder_service.delete_file_from_folder(folder_id, file_name)
    print(f"File '{file_name}' deleted from Folder ID: {folder_id}")

def delete_folder():
    folder_id = input("Enter the folder ID to delete: ")
    folder_service.delete_folder(folder_id)
    print(f"Folder ID {folder_id} and all its contents have been deleted.")

def list_files_in_folder():
    folder_id = input("Enter the folder ID: ")
    folder = folder_repo.get_folder(folder_id)
    if folder:
        print(f"Files in folder '{folder.folder_name}':")
        for file in folder.files:
            print(f" - {file.file_name}: {file.upload_url}")
    else:
        print(f"Folder ID {folder_id} not found.")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            create_folder()
        elif choice == '2':
            add_file_to_folder()
        elif choice == '3':
            move_folder()
        elif choice == '4':
            delete_file_from_folder()
        elif choice == '5':
            delete_folder()
        elif choice == '6':
            list_files_in_folder()
        elif choice == '7':
            print("Exiting the program.")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


import os
import shutil
import filecmp
import tkinter as tk
from tkinter import filedialog
import re

# Function to create a backup of the configuration file
def create_backup(cfg_file_path, backup_path):
    shutil.copy(cfg_file_path, backup_path)

# Function to validate if the original and backup files are identical
def validate_files_identical(cfg_file_path, backup_path):
    return filecmp.cmp(cfg_file_path, backup_path)

# Function to undo modifications to the configuration file
def undo_modify_cfg_file(cfg_file_path, backup_path):
    try:
        with open(backup_path, 'r') as backup_file:
            backup_content = backup_file.read()

        with open(cfg_file_path, 'w') as cfg_file:
            cfg_file.write(backup_content)

        result = validate_files_identical(cfg_file_path, backup_path)
        if result:
            os.remove(backup_path)
            result_label.config(text="Undo successful! Backup deleted.")
        else:
            result_label.config(text="Undo failed! Files are not identical. Skipping folder.")

    except FileNotFoundError:
        result_label.config(text="Error: Backup file not found.")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

# Function to initiate the undo process for all folders
def undo_process_folders():
    parent_directory = entry_directory.get()
    if parent_directory:
        undo_process_folders_helper(parent_directory)
    else:
        result_label.config(text="Please select a valid parent directory.")

# Helper function to recursively process all folders and undo modifications
def undo_process_folders_helper(parent_directory):
    for root, dirs, files in os.walk(parent_directory):
        if 'notescopy.cfg' in files:
            cfg_file_path = os.path.join(root, 'notes.cfg')
            backup_path = os.path.join(root, 'notescopy.cfg')

            undo_modify_cfg_file(cfg_file_path, backup_path)

# Function to modify the configuration file
def modify_cfg_file(cfg_file_path):
    try:
        backup_path = cfg_file_path.replace('notes.cfg', 'notescopy.cfg')

        if not os.path.exists(backup_path):
            create_backup(cfg_file_path, backup_path)
            msg = "File modified successfully!\nBackup created at: {}".format(backup_path)
        else:
            msg = "Skipping folder. File modified at: {}".format(cfg_file_path)

        with open(cfg_file_path, 'r') as file:
            content = file.read()

        content = re.sub(r'"input_type": \d+,', '"input_type": 0,', content)
        content = re.sub(r'"note_modifier": \d+,', '"note_modifier": 1,', content)

        with open(cfg_file_path, 'w') as file:
            file.write(content)

        result_label.config(text=msg)

    except FileNotFoundError:
        result_label.config(text="Error: File not found.")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

# Function to process all folders in the parent directory
def process_folders(parent_directory):
    for root, dirs, files in os.walk(parent_directory):
        if 'notes.cfg' in files:
            cfg_file_path = os.path.join(root, 'notes.cfg')
            backup_path = os.path.join(root, 'notescopy.cfg')

            modify_cfg_file(cfg_file_path)

# Function to open a directory selection dialog
def browse_directory():
    directory_path = filedialog.askdirectory(title="Select Parent Directory")
    if directory_path:
        entry_directory.delete(0, tk.END)
        entry_directory.insert(0, directory_path)

# Function to initiate the folder processing and modification
def process_folders_and_modify():
    parent_directory = entry_directory.get()
    if parent_directory:
        process_folders(parent_directory)
    else:
        result_label.config(text="Please select a valid parent directory.")

# Create the main application window with a fixed size and disable resizing
root = tk.Tk()
root.title("CFG File Modifier")
root.geometry("430x200")  # Set the window size to 430x200 pixels
root.resizable(False, False)  # Disable window resizing

# Create and place widgets in the main window
label_directory = tk.Label(root, text="Parent Directory:", wraplength=150, anchor="w")
label_directory.grid(row=0, column=0, pady=10, padx=5, sticky="w")

entry_directory = tk.Entry(root, width=40)
entry_directory.grid(row=0, column=1, pady=10, padx=5, sticky="w")

button_browse_directory = tk.Button(root, text="Browse", command=browse_directory)
button_browse_directory.grid(row=0, column=2, pady=10, padx=5, sticky="e")

button_process_folders = tk.Button(root, text="Process Folders", command=process_folders_and_modify)
button_process_folders.grid(row=1, column=1, pady=10, padx=5, sticky="ew")

button_undo = tk.Button(root, text="Undo", command=undo_process_folders)
button_undo.grid(row=2, column=1, pady=10, padx=5, sticky="ew")

result_label = tk.Label(root, text="", wraplength=380, anchor="w")
result_label.grid(row=3, column=0, columnspan=3, pady=10, padx=5, sticky="w")

# Run the main loop of the application
root.mainloop()

import os
import shutil
import filecmp
import tkinter as tk
from tkinter import filedialog

def create_backup(cfg_file_path, backup_path):
    shutil.copy(cfg_file_path, backup_path)

def validate_files_identical(cfg_file_path, backup_path):
    return filecmp.cmp(cfg_file_path, backup_path)

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

def undo_process_folders():
    parent_directory = entry_directory.get()
    if parent_directory:
        undo_process_folders_helper(parent_directory)
    else:
        result_label.config(text="Please select a valid parent directory.")

def undo_process_folders_helper(parent_directory):
    for root, dirs, files in os.walk(parent_directory):
        if 'notescopy.cfg' in files:
            cfg_file_path = os.path.join(root, 'notes.cfg')
            backup_path = os.path.join(root, 'notescopy.cfg')

            undo_modify_cfg_file(cfg_file_path, backup_path)

def create_backup(cfg_file_path, backup_path):
    shutil.copy(cfg_file_path, backup_path)

def modify_cfg_file(cfg_file_path):
    try:
        backup_path = cfg_file_path.replace('notes.cfg', 'notescopy.cfg')

        if not os.path.exists(backup_path):
            create_backup(cfg_file_path, backup_path)

            with open(cfg_file_path, 'r') as file:
                lines = file.readlines()

            with open(cfg_file_path, 'w') as file:
                for line in lines:
                    # Modify the line as needed
                    if '"input_type":' in line:
                        line = line.replace('"input_type": 1,', '"input_type": 0,')
                        line = line.replace('"input_type": 2,', '"input_type": 0,')
                        line = line.replace('"input_type": 3,', '"input_type": 0,')
                        # Add more replacements if needed for other values of x
                    elif '"note_modifier":' in line:
                        line = line.replace('"note_modifier": 0,', '"note_modifier": 1,')
                        line = line.replace('"note_modifier": 2,', '"note_modifier": 1,')
                        # Add more replacements if needed for other values of x

                    file.write(line)

            result_label.config(text="File modified successfully!\nBackup created at: {}".format(backup_path))
        else:
            result_label.config(text="Skipping folder. Backup already exists at: {}".format(backup_path))

    except FileNotFoundError:
        result_label.config(text="Error: File not found.")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

def process_folders(parent_directory):
    for root, dirs, files in os.walk(parent_directory):
        if 'notes.cfg' in files:
            cfg_file_path = os.path.join(root, 'notes.cfg')
            backup_path = os.path.join(root, 'notescopy.cfg')

            if not os.path.exists(backup_path):
                create_backup(cfg_file_path, backup_path)

                with open(cfg_file_path, 'r') as file:
                    lines = file.readlines()

                with open(cfg_file_path, 'w') as file:
                    for line in lines:
                        # Modify the line as needed
                        if '"input_type":' in line:
                            line = line.replace('"input_type": 1,', '"input_type": 0,')
                            line = line.replace('"input_type": 2,', '"input_type": 0,')
                            line = line.replace('"input_type": 3,', '"input_type": 0,')
                            # Add more replacements if needed for other values of x
                        elif '"note_modifier":' in line:
                            line = line.replace('"note_modifier": 0,', '"note_modifier": 1,')
                            line = line.replace('"note_modifier": 2,', '"note_modifier": 1,')
                            # Add more replacements if needed for other values of x

                        file.write(line)

                result_label.config(text="File modified successfully!\nBackup created at: {}".format(backup_path))
            else:
                result_label.config(text="Skipping folder. Backup already exists at: {}".format(backup_path))

    # Resize the window after processing folders
    resize_window()

def browse_directory():
    directory_path = filedialog.askdirectory(title="Select Parent Directory")
    if directory_path:
        entry_directory.delete(0, tk.END)
        entry_directory.insert(0, directory_path)

def process_folders_and_modify():
    parent_directory = entry_directory.get()
    if parent_directory:
        process_folders(parent_directory)
    else:
        result_label.config(text="Please select a valid parent directory.")

def undo_process_folders():
    parent_directory = entry_directory.get()
    if parent_directory:
        undo_process_folders_helper(parent_directory)
    else:
        result_label.config(text="Please select a valid parent directory.")

def undo_process_folders_helper(parent_directory):
    for root, dirs, files in os.walk(parent_directory):
        if 'notescopy.cfg' in files:
            cfg_file_path = os.path.join(root, 'notes.cfg')
            backup_path = os.path.join(root, 'notescopy.cfg')

            undo_modify_cfg_file(cfg_file_path, backup_path)

    # Resize the window after undoing folders
    resize_window()

# Function to resize the window
def resize_window():
    root.update_idletasks()
    root.geometry("")

# Create the main window
root = tk.Tk()
root.title("CFG File Modifier")

# Create and place widgets
label_directory = tk.Label(root, text="Beat Banger Folder:")
label_directory.grid(row=0, column=0, pady=10)

entry_directory = tk.Entry(root, width=40)
entry_directory.grid(row=0, column=1, pady=10)

button_browse_directory = tk.Button(root, text="Browse", command=browse_directory)
button_browse_directory.grid(row=0, column=2, pady=10)

button_process_folders = tk.Button(root, text="Activate EZ Mode", command=process_folders_and_modify)
button_process_folders.grid(row=1, column=1, pady=10)

button_undo = tk.Button(root, text="Restore regular notes", command=undo_process_folders)
button_undo.grid(row=2, column=1, pady=10)

result_label = tk.Label(root, text="")
result_label.grid(row=3, column=1, pady=10)

# Call the resize_window function to set the initial size
resize_window()

# Run the main loop
root.mainloop()

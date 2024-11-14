import tkinter as tk
from tkinter import Entry

# Initialize the main application window
root = tk.Tk()
root.title("12x6 Grid")

# Create a 12x6 grid of Entry widgets
entries = []

for row in range(12):  # 12 rows
    row_entries = []
    for col in range(6):  # 6 columns
        # Create an Entry widget for each cell
        entry = Entry(root, width=10, justify='center')
        entry.grid(row=row, column=col, padx=5, pady=5)  # Position in grid with padding
        row_entries.append(entry)
    entries.append(row_entries)

# Function to set the first row as headers
def set_row_as_headers(row_index, headers):
    for col, header_text in enumerate(headers):
        entries[row_index][col].delete(0, tk.END)  # Clear any existing text
        entries[row_index][col].insert(0, header_text)  # Insert header text
        #entries[row_index][col].config(state='readonly')  # Make the cell read-only

# Define header texts for each column in row 1
header_texts = ["", "", "Person 1", "Person 2", "Person 3", "Person 4"]

# Update row 1 to be headers
set_row_as_headers(0, header_texts)

# Run the application
root.mainloop()

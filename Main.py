import tkinter as tk
from tkinter import Entry, StringVar

# Initialize the main application window
root = tk.Tk()
root.title("Better Bill Splitter")

# Create a 12x6 grid of Entry widgets
entries = []
vars = [] # A list to store StringVar objects for tracing

for row in range(13):  # 12 rows
    row_entries = []
    row_vars = []
    for col in range(6):  # 6 columns
        var = StringVar() # Create a StringVar for each cell
        # Create an Entry widget for each cell
        entry = Entry(root, textvariable=var, width=10, justify='center') #added "textvariable=var to link entry with var"
        entry.grid(row=row, column=col, padx=5, pady=5)  # Position in grid with padding
        row_entries.append(entry)
        row_vars.append(var) #added
    entries.append(row_entries)
    vars.append(row_vars) #added

# Function to set the first row as headers
def set_row_as_headers(row_index, headers):
    for col, header_text in enumerate(headers):
        entries[row_index][col].delete(0, tk.END)  # Clear any existing text
        entries[row_index][col].insert(0, header_text)  # Insert header text
        entries[row_index][col].config(font=("Arial", 10,"bold"))
# Function to set first column as headers
def set_column_as_headers(col_index, headers):
    for row, header_text in enumerate(headers):
        entries[row][col_index].delete(0, tk.END)  # Clear any existing text
        entries[row][col_index].insert(0, header_text)  # Insert header text
        entries[row][col_index].config(font=("Arial", 10, "bold"))

# Define header texts for each cell in column and rows
row_header_texts = ["", "", "Person 1", "Person 2", "Person 3", "Person 4"]
column_header_texts = ["", "Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "", "subtotal", "Tip", "Tax", "Tip w/Tax", "TOTAL"]
total_section_default_values = ["15%", "9.5%", "0%"]

# Update row 1 and col 1 to be headers
set_row_as_headers(0, row_header_texts)
set_column_as_headers(0, column_header_texts)

# Make cells read-only
#blank spaces in row 1 col 1-2
for col in range(0, 2):
    entries[0][col].config(state='readonly')
#the total section
for row in range(7, 13):
    for col in range(0, 6):
        entries[row][col].config(state='readonly')
#add an editable field for the tip, tax, tip w/tax
for index, row in enumerate(range(9, 12)):
    entries[row][1].config(state='normal')
    entries[row][1].delete(0, tk.END)
    entries[row][1].insert(0, total_section_default_values[index])

def calculate_subtotal(*args):
    for col in range(2, 6):
        subtotal = 0
        for row in range(1, 7):
            try:
                cell_value = float(vars[row][col].get()) if vars[row][col].get() else 0
                subtotal += cell_value
            except ValueError:
                pass
        # Temporarily make the cell in row 8 editable
        entries[8][col].config(state='normal')
        entries[8][col].delete(0, tk.END)
        entries[8][col].insert(0, f"${subtotal:.2f}")
        # Set the cell back to read-only
        entries[8][col].config(state='readonly')
# Set up trace for cells in rows 2 to 7 and columns 3 to 6
for row in range(1, 7):  # Rows 2 to 7 (indices 1 to 6)
    for col in range(2, 6):  # Columns 3 to 6 (indices 2 to 5)
        # Add a trace on each cell's StringVar to auto-calculate subtotal on change
        vars[row][col].trace_add("write", calculate_subtotal)

# Run the application
root.mainloop()

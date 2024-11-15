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
#blank spaces in row 2-7 col 2
for row in range(1, 7):
    entries[row][1].config(state='readonly')
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

def calculate_tip(*args):
    calculate_subtotal() # this needs to be run first because the function was calculating tip before or at the same time the subtotal was
    try:
        # Retrieve the tip percentage from row 10, column 2
        tip_percentage = float(vars[9][1].get().strip('%')) / 100 if vars[9][1].get() else 0
    except ValueError:
        tip_percentage = 0

    # Only calculate if the "Tip" percentage is more than 0%
    if tip_percentage > 0:
        # Set "Tip w/tax %" (row 12, column 2) to 0%
        entries[11][1].delete(0, tk.END)
        entries[11][1].insert(0, "0%")

    for col in range(2, 6):  # Columns 3 to 6
        try:
            # Get the subtotal from row 8
            subtotal = float(vars[8][col].get().strip('$')) if vars[8][col].get() else 0
            # Calculate the tip based on the subtotal and tip percentage
            tip_amount = subtotal * tip_percentage
        except ValueError:
            tip_amount = 0

        # Temporarily make the cell in row 10 editable, then update and revert to read-only
        entries[9][col].config(state='normal')
        entries[9][col].delete(0, tk.END)
        entries[9][col].insert(0, f"${tip_amount:.2f}")
        entries[9][col].config(state='readonly')

#calc tax
def calculate_tax(*args):
    calculate_subtotal() # this needs to be run first because the function was calculating tip before or at the same time the subtotal was
    try:
        # Retrieve the tax percentage from row 11, column 2
        tax_percentage = float(vars[10][1].get().strip('%')) / 100 if vars[10][1].get() else 0
    except ValueError:
        tax_percentage = 0

    for col in range(2, 6):  # Columns 3 to 6
        try:
            # Get the subtotal from row 8
            subtotal = float(vars[8][col].get().strip('$')) if vars[8][col].get() else 0
            # Calculate the tax based on the subtotal and tax percentage
            tax_amount = subtotal * tax_percentage
        except ValueError:
            tax_amount = 0

        # Temporarily make the cell in row 10 editable, then update and revert to read-only
        entries[10][col].config(state='normal')
        entries[10][col].delete(0, tk.END)
        entries[10][col].insert(0, f"${tax_amount:.2f}")
        entries[10][col].config(state='readonly')

#calc tip w/tax
def calculate_tip_with_tax(*args):
    calculate_subtotal() # this needs to be run first because the function was calculating tip before or at the same time the subtotal was
    calculate_tax()
    try:
        # Retrieve the tax percentage from row 11, column 2
        tip_with_tax_percentage = float(vars[11][1].get().strip('%')) / 100 if vars[11][1].get() else 0
    except ValueError:
        tip_with_tax_percentage = 0

    # Only calculate if the "Tip w/Tax" percentage is more than 0%
    if tip_with_tax_percentage > 0:
        # Set "Tip %" (row 10, column 2) to 0%
        entries[9][1].delete(0, tk.END)
        entries[9][1].insert(0, "0%")

        for col in range(2, 6):  # Columns 3 to 6
            try:
                # Get the subtotal and tax amounts from rows 8 and 11
                subtotal = float(vars[8][col].get().strip('$')) if vars[8][col].get() else 0
                tax = float(vars[10][col].get().strip('$')) if vars[10][col].get() else 0
                # Calculate the tip with tax based on subtotal + tax
                tip_with_tax_amount = (subtotal + tax) * (tip_with_tax_percentage)
            except ValueError:
                tip_with_tax_amount = 0  # Default to 0 if any value is invalid

            # Temporarily make the cell in row 12 editable, then update and revert to read-only
            entries[11][col].config(state='normal')
            entries[11][col].delete(0, tk.END)
            entries[11][col].insert(0, f"${tip_with_tax_amount:.2f}")
            entries[11][col].config(state='readonly')

# Set up trace for cells in rows 2 to 7 and columns 3 to 6
for row in range(1, 7):  # Rows 2 to 7 (indices 1 to 6)
    for col in range(2, 6):  # Columns 3 to 6 (indices 2 to 5)
        # Add a trace on each cell's StringVar to auto-calculate subtotal on change
        vars[row][col].trace_add("write", calculate_subtotal)
        vars[row][col].trace_add("write", calculate_tip)
        vars[row][col].trace_add("write", calculate_tax)
        vars[row][col].trace_add("write", calculate_tip_with_tax)

# Set up trace for tip, tax, and tip w/tax percentages
vars[9][1].trace_add("write", calculate_tip)
vars[10][1].trace_add("write", calculate_tax)
vars[11][1].trace_add("write", calculate_tip_with_tax)

# Run the application
root.mainloop()

import customtkinter as ctk
import tkinter as tk

# Test correct customtkinter dropdown syntax
app = ctk.CTk()
app.title("CTK Dropdown Test")
app.geometry("400x200")

var = tk.StringVar()
dropdown = ctk.CTkComboBox(app, variable=var, width=300)
dropdown.pack(pady=20, padx=20)

# Try different ways to set values
test_values = ["msedge.exe (PID: 1528)", "EXCEL.EXE (PID: 34628)"]

print("Method 1: Using configure")
try:
    dropdown.configure(values=test_values)
    print("✓ configure() worked")
except Exception as e:
    print(f"✗ configure() failed: {e}")

print("Method 2: Using direct assignment")
try:
    dropdown['values'] = test_values
    print("✓ direct assignment worked")
except Exception as e:
    print(f"✗ direct assignment failed: {e}")

print("Method 3: Check current values")
try:
    current_values = dropdown.cget('values') if hasattr(dropdown, 'cget') else dropdown['values']
    print(f"Current values: {current_values}")
except Exception as e:
    print(f"✗ getting values failed: {e}")

app.mainloop()

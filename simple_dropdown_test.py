import customtkinter as ctk
import tkinter as tk

class SimpleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Simple Dropdown Test")
        self.geometry("500x200")
        
        # Create dropdown
        self.var = tk.StringVar()
        self.dropdown = ctk.CTkComboBox(
            self,
            variable=self.var,
            width=400
        )
        self.dropdown.pack(pady=20, padx=20)
        
        # Test with hardcoded values
        test_values = [
            "msedge.exe (PID: 1528)",
            "EXCEL.EXE (PID: 34628)", 
            "Spotify.exe (PID: 14672)",
            "chrome.exe (PID: 1234)",
            "firefox.exe (PID: 5678)"
        ]
        
        print("Setting dropdown values...")
        print(f"Values: {test_values}")
        
        self.dropdown['values'] = test_values
        self.dropdown.set(test_values[0])
        
        print(f"Set dropdown to: {test_values[0]}")
        print(f"Current dropdown value: {self.var.get()}")
        
        # Add button to check current value
        check_btn = ctk.CTkButton(
            self,
            text="Check Selection",
            command=self.check_selection
        )
        check_btn.pack(pady=10)
        
    def check_selection(self):
        current = self.var.get()
        print(f"Current selection: {current}")
        print(f"Dropdown values: {self.dropdown['values']}")

if __name__ == "__main__":
    app = SimpleApp()
    app.mainloop()

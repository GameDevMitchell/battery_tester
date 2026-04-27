import customtkinter as ctk
import tkinter as tk
from monitor import get_running_processes

class TestApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Test Dropdown")
        self.geometry("400x300")
        
        # Test the process dropdown directly
        self.process_var = tk.StringVar()
        self.process_dropdown = ctk.CTkComboBox(
            self,
            variable=self.process_var,
            width=300
        )
        self.process_dropdown.pack(pady=20, padx=20)
        
        # Load processes
        self.load_processes()
        
        # Add refresh button
        refresh_btn = ctk.CTkButton(
            self,
            text="Refresh",
            command=self.load_processes
        )
        refresh_btn.pack(pady=10)
        
        # Add label to show current selection
        self.selection_label = ctk.CTkLabel(self, text="Selected: None")
        self.selection_label.pack(pady=10)
        
        # Bind selection change
        self.process_dropdown.bind("<<ComboboxSelected>>", self.on_select)
        
    def load_processes(self):
        try:
            processes = get_running_processes()
            process_list = [f"{proc['name']} (PID: {proc['pid']})" for proc in processes]
            print(f"Found {len(process_list)} processes")
            print("First 5:", process_list[:5])
            
            self.process_dropdown['values'] = process_list
            
            if process_list and not self.process_var.get():
                self.process_dropdown.set(process_list[0])
                self.selection_label.configure(text=f"Selected: {process_list[0]}")
                
        except Exception as e:
            print(f"Error: {e}")
            
    def on_select(self, event):
        selection = self.process_var.get()
        self.selection_label.configure(text=f"Selected: {selection}")

if __name__ == "__main__":
    app = TestApp()
    app.mainloop()

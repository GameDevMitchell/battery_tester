# main.py
# Entry point for the Battery Performance Tester application.
# Run this file to launch the GUI application.

from ui.app_window import AppWindow

# The if __name__ == "__main__": block ensures that the code inside it
# only runs when this script is executed directly (not when imported as a module)
if __name__ == "__main__":
    # Create the main application window
    app = AppWindow()
    
    # Start the Tkinter event loop - this keeps the application running
    # and responsive to user interactions until the window is closed
    app.mainloop()

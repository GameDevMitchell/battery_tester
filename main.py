# main.py
# Entry point for the spectacular Battery Performance Tester application.
# Run this file to launch the professional GUI with modern design.

from ui.app_window_redesigned import AppWindowRedesigned

# The if __name__ == "__main__": block ensures that the code inside it
# only runs when this script is executed directly (not when imported as a module)
if __name__ == "__main__":
    # Create the main application window
    app = AppWindowRedesigned()
    
    # Start the Tkinter event loop - this keeps the application running
    # and responsive to user interactions until the window is closed
    app.mainloop()



from ui.app_window_working import AppWindowWorking

# The if __name__ == "__main__": block ensures that the code inside it
# only runs when this script is executed directly (not when imported as a module)
if __name__ == "__main__":
    # Create the main application window
    app = AppWindowWorking()
    
    # Start the Tkinter event loop - this keeps the application running
    # and responsive to user interactions until the window is closed
    app.mainloop()

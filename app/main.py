import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        from gui import ConverterApp
        
        app = ConverterApp()
        app.mainloop()
    except Exception as e:
        error_message = f"Error starting application: {str(e)}\n\n{traceback.format_exc()}"
        print(error_message)
        
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()  
            messagebox.showerror("Application Error", error_message)
            root.destroy()
        except:
            pass

if __name__ == "__main__":
    main()
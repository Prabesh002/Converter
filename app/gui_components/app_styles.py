from tkinter import ttk

DARK_BG = "#1E1E1E"
LIGHT_BG = "#252526"
ACCENT_COLOR = "#007ACC"
TEXT_COLOR = "#D4D4D4"
HIGHLIGHT_COLOR = "#3C3C3C"
SUCCESS_COLOR = "#6A9955"
ERROR_COLOR = "#F14C4C"

FONT = ("Segoe UI", 10)
TITLE_FONT = ("Segoe UI", 14, "bold")
BUTTON_FONT = ("Segoe UI", 10)

def setup_styles():
    """Configure and return the application styles"""
    style = ttk.Style()
    style.theme_use('clam')

    style.configure('TFrame', background=DARK_BG)
    

    style.configure('TButton', 
                    background=ACCENT_COLOR, 
                    foreground='white', 
                    font=BUTTON_FONT,
                    borderwidth=0)
    style.map('TButton', 
              background=[('active', '#0090EA'), ('pressed', '#005A9E')])
    

    style.configure('TProgressbar', 
                    background=ACCENT_COLOR,
                    troughcolor=LIGHT_BG,
                    borderwidth=0)
    

    style.configure('TLabel', 
                    background=DARK_BG, 
                    foreground=TEXT_COLOR, 
                    font=FONT)
    

    style.configure('TCheckbutton', 
                    background=LIGHT_BG,
                    foreground=TEXT_COLOR,
                    font=FONT)
    style.map('TCheckbutton',
              background=[('active', LIGHT_BG)],
              foreground=[('active', TEXT_COLOR)])
    
    return style
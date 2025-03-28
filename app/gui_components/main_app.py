import tkinter as tk
import os
import sys
import json
from .ui_builder import UIBuilder
from .app_functions import AppFunctions
from .app_styles import setup_styles, DARK_BG

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

with open(resource_path("config.json"), "r") as f:
    config = json.load(f)

class ConverterApp(tk.Tk):
    """Main application class for the Video Converter"""
    
    def __init__(self):
        super().__init__()
        self.title(config.get("app_title", "Video Converter"))
        self.geometry("900x700")
        self.configure(bg=DARK_BG)
        self.minsize(800, 600)
        
        # Load icon
        icon_path = config.get("app_icon")
        if icon_path and os.path.exists(resource_path(icon_path)):
            try:
                from PIL import ImageTk, Image
                icon = ImageTk.PhotoImage(file=resource_path(icon_path))
                self.iconphoto(True, icon)
            except Exception as e:
                print(f"Error loading icon: {e}")
        
        self.style = setup_styles()
        
        self.initialize_variables()
        
        self.functions = AppFunctions(self)
        
        self.ui_builder = UIBuilder(self)
        self.ui_builder.create_widgets()
        
        self.update_log("Application started. Ready to process videos.")
    

    def update_log(self, log_text, level="info"):
        self.functions.update_log(log_text, level)
    
    def update_progress(self, value, status_text=None):
        self.functions.update_progress(value, status_text)
    
    def select_video(self):
        self.functions.select_video()
    
    def start_processing(self):
        self.functions.start_processing()
    
    def on_style_selected(self, event):
        self.functions.on_style_selected(event)
    
    def get_style_description(self):
        return self.functions.get_style_description()
    
    def get_custom_params(self):
        return self.functions.get_custom_params()
    
    def reset_form(self):
        self.functions.reset_form()
    
    def initialize_variables(self):
        """Initialize all the variables used in the application"""
        self.progress_var = tk.DoubleVar(value=0)
        self.video_path = tk.StringVar()
        self.output_name = tk.StringVar()
        self.fps = tk.IntVar(value=config["fps"])
        self.edge_min = tk.IntVar(value=config["edge_threshold"][0])
        self.edge_max = tk.IntVar(value=config["edge_threshold"][1])
        self.distortion = tk.DoubleVar(value=config["distortion_strength"])
        
        import core
        self.available_styles = core.get_available_styles() if hasattr(core, 'get_available_styles') else ["faith", "classic_pixel", "glitch", "legacy_edge"]
        self.selected_style = tk.StringVar(value=config.get("default_style", "faith"))
        
        self.pixel_size = tk.IntVar(value=4)
        self.use_dithering = tk.BooleanVar(value=True)
        self.contrast = tk.DoubleVar(value=1.5)
        self.noise_level = tk.DoubleVar(value=0.2)
        
        self.export_original_frames = tk.BooleanVar(value=False)
        self.export_nobg_frames = tk.BooleanVar(value=True)
        self.export_processed_frames = tk.BooleanVar(value=False)
        self.create_final_video = tk.BooleanVar(value=True)
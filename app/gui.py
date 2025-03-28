import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import core
import os
import subprocess
from PIL import Image, ImageTk
import threading

with open("config.json", "r") as f:
    config = json.load(f)

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

class ConverterApp(tk.Tk):
    from PIL import Image, ImageTk
    import json
    from tkinter import filedialog, messagebox, ttk
    
    with open("config.json", "r") as f:
        config = json.load(f)

    def __init__(self):
        super().__init__()
        self.title(config.get("app_title", "Video Converter"))
        self.geometry("900x700")
        self.configure(bg=DARK_BG)
        self.minsize(800, 600)
        
        icon_path = config.get("app_icon")
        if icon_path and os.path.exists(icon_path):
            try:
                icon = ImageTk.PhotoImage(file=icon_path)
                self.iconphoto(True, icon)
            except Exception as e:
                print(f"Error loading icon: {e}")
        

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background=DARK_BG)
        self.style.configure('TButton', 
                             background=ACCENT_COLOR, 
                             foreground='white', 
                             font=BUTTON_FONT,
                             borderwidth=0)
        self.style.map('TButton', 
                      background=[('active', '#0090EA'), ('pressed', '#005A9E')])
        self.style.configure('TProgressbar', 
                             background=ACCENT_COLOR,
                             troughcolor=LIGHT_BG,
                             borderwidth=0)
        self.style.configure('TLabel', 
                             background=DARK_BG, 
                             foreground=TEXT_COLOR, 
                             font=FONT)
        self.style.configure('TCheckbutton', 
                             background=LIGHT_BG,
                             foreground=TEXT_COLOR,
                             font=FONT)
        self.style.map('TCheckbutton',
                      background=[('active', LIGHT_BG)],
                      foreground=[('active', TEXT_COLOR)])
        
        self.progress_var = tk.DoubleVar(value=0)
        self.video_path = tk.StringVar()
        self.output_name = tk.StringVar()
        self.fps = tk.IntVar(value=config["fps"])
        self.edge_min = tk.IntVar(value=config["edge_threshold"][0])
        self.edge_max = tk.IntVar(value=config["edge_threshold"][1])
        self.distortion = tk.DoubleVar(value=config["distortion_strength"])
        
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
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(main_frame, text="Video Converter", 
                              font=TITLE_FONT, bg=DARK_BG, fg=ACCENT_COLOR)
        title_label.pack(pady=(0, 20))
        
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        file_frame = tk.Frame(left_panel, bg=LIGHT_BG, padx=15, pady=15)
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(file_frame, text="Video File", font=FONT, bg=LIGHT_BG, fg=TEXT_COLOR).pack(anchor=tk.W)
        
        file_input_frame = tk.Frame(file_frame, bg=LIGHT_BG)
        file_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.video_path_entry = tk.Entry(file_input_frame, textvariable=self.video_path,
                                        font=FONT, bg=DARK_BG, fg=TEXT_COLOR, 
                                        insertbackground=TEXT_COLOR, relief=tk.FLAT)
        self.video_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5, padx=(0, 5))
        
        browse_btn = ttk.Button(file_input_frame, text="Browse", command=self.select_video)
        browse_btn.pack(side=tk.RIGHT)
        
        output_frame = tk.Frame(left_panel, bg=LIGHT_BG, padx=15, pady=15)
        output_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(output_frame, text="Output Folder Name", font=FONT, bg=LIGHT_BG, fg=TEXT_COLOR).pack(anchor=tk.W)
        
        self.output_name_entry = tk.Entry(output_frame, textvariable=self.output_name,
                                         font=FONT, bg=DARK_BG, fg=TEXT_COLOR, 
                                         insertbackground=TEXT_COLOR, relief=tk.FLAT)
        self.output_name_entry.pack(fill=tk.X, expand=True, ipady=5, pady=(5, 0))
        
        options_frame = tk.Frame(left_panel, bg=LIGHT_BG, padx=15, pady=15)
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(options_frame, text="Processing Options", font=FONT, bg=LIGHT_BG, fg=TEXT_COLOR).pack(anchor=tk.W)
        
        export_orig_check = ttk.Checkbutton(options_frame, text="Export Original Frames", 
                                          variable=self.export_original_frames, style='TCheckbutton')
        export_orig_check.pack(anchor=tk.W, pady=(5, 2))
        
        export_nobg_check = ttk.Checkbutton(options_frame, text="Export Frames with Background Removed", 
                                          variable=self.export_nobg_frames, style='TCheckbutton')
        export_nobg_check.pack(anchor=tk.W, pady=2)
        
        export_proc_check = ttk.Checkbutton(options_frame, text="Export Processed Frames", 
                                          variable=self.export_processed_frames, style='TCheckbutton')
        export_proc_check.pack(anchor=tk.W, pady=2)
        
        create_video_check = ttk.Checkbutton(options_frame, text="Create Final Video", 
                                           variable=self.create_final_video, style='TCheckbutton')
        create_video_check.pack(anchor=tk.W, pady=2)
        
        params_frame = tk.Frame(left_panel, bg=LIGHT_BG, padx=15, pady=15)
        params_frame.pack(fill=tk.X)
        
        tk.Label(params_frame, text="Parameters", font=FONT, bg=LIGHT_BG, fg=TEXT_COLOR).pack(anchor=tk.W)
        
        fps_frame = tk.Frame(params_frame, bg=LIGHT_BG, pady=5)
        fps_frame.pack(fill=tk.X)
        
        tk.Label(fps_frame, text="FPS:", width=15, anchor=tk.W, 
                bg=LIGHT_BG, fg=TEXT_COLOR, font=FONT).pack(side=tk.LEFT)
        
        fps_slider = tk.Scale(fps_frame, from_=1, to=60, variable=self.fps,
                             orient=tk.HORIZONTAL, bg=LIGHT_BG, fg=TEXT_COLOR,
                             highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                             activebackground=ACCENT_COLOR, troughcolor=DARK_BG)
        fps_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        edge_min_frame = tk.Frame(params_frame, bg=LIGHT_BG, pady=5)
        edge_min_frame.pack(fill=tk.X)
        
        tk.Label(edge_min_frame, text="Min Edge Threshold:", width=15, anchor=tk.W,
                bg=LIGHT_BG, fg=TEXT_COLOR, font=FONT).pack(side=tk.LEFT)
        
        edge_min_slider = tk.Scale(edge_min_frame, from_=0, to=100, variable=self.edge_min,
                                  orient=tk.HORIZONTAL, bg=LIGHT_BG, fg=TEXT_COLOR,
                                  highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                                  activebackground=ACCENT_COLOR, troughcolor=DARK_BG)
        edge_min_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        edge_max_frame = tk.Frame(params_frame, bg=LIGHT_BG, pady=5)
        edge_max_frame.pack(fill=tk.X)
        
        tk.Label(edge_max_frame, text="Max Edge Threshold:", width=15, anchor=tk.W,
                bg=LIGHT_BG, fg=TEXT_COLOR, font=FONT).pack(side=tk.LEFT)
        
        edge_max_slider = tk.Scale(edge_max_frame, from_=100, to=500, variable=self.edge_max,
                                  orient=tk.HORIZONTAL, bg=LIGHT_BG, fg=TEXT_COLOR,
                                  highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                                  activebackground=ACCENT_COLOR, troughcolor=DARK_BG)
        edge_max_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        distortion_frame = tk.Frame(params_frame, bg=LIGHT_BG, pady=5)
        distortion_frame.pack(fill=tk.X)
        
        tk.Label(distortion_frame, text="Distortion Strength:", width=15, anchor=tk.W,
                bg=LIGHT_BG, fg=TEXT_COLOR, font=FONT).pack(side=tk.LEFT)
        
        distortion_slider = tk.Scale(distortion_frame, from_=0, to=10, variable=self.distortion,
                                    orient=tk.HORIZONTAL, bg=LIGHT_BG, fg=TEXT_COLOR,
                                    highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                                    activebackground=ACCENT_COLOR, troughcolor=DARK_BG,
                                    resolution=0.1)
        distortion_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        style_frame = tk.Frame(left_panel, bg=LIGHT_BG, padx=15, pady=15)
        style_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Label(style_frame, text="Art Style", font=FONT, bg=LIGHT_BG, fg=TEXT_COLOR).pack(anchor=tk.W)
        
        style_combobox = ttk.Combobox(style_frame, textvariable=self.selected_style, 
                                     values=self.available_styles, state="readonly")
        style_combobox.pack(fill=tk.X, pady=(5, 10))
        style_combobox.bind("<<ComboboxSelected>>", self.on_style_selected)

        self.style_desc_label = tk.Label(style_frame, text=self.get_style_description(), 
                                       font=("Segoe UI", 8), bg=LIGHT_BG, fg=TEXT_COLOR,
                                       wraplength=300, justify=tk.LEFT)
        self.style_desc_label.pack(fill=tk.X, pady=(0, 10))

        self.custom_params_frame = tk.Frame(style_frame, bg=LIGHT_BG)
        
        pixel_frame = tk.Frame(self.custom_params_frame, bg=LIGHT_BG, pady=5)
        pixel_frame.pack(fill=tk.X)
        tk.Label(pixel_frame, text="Pixel Size:", width=15, anchor=tk.W,
                bg=LIGHT_BG, fg=TEXT_COLOR, font=FONT).pack(side=tk.LEFT)
        pixel_slider = tk.Scale(pixel_frame, from_=1, to=8, variable=self.pixel_size,
                               orient=tk.HORIZONTAL, bg=LIGHT_BG, fg=TEXT_COLOR,
                               highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                               activebackground=ACCENT_COLOR, troughcolor=DARK_BG)
        pixel_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        dither_frame = tk.Frame(self.custom_params_frame, bg=LIGHT_BG, pady=5)
        dither_frame.pack(fill=tk.X)
        dither_check = ttk.Checkbutton(dither_frame, text="Use Dithering", 
                                      variable=self.use_dithering, style='TCheckbutton')
        dither_check.pack(anchor=tk.W)
        
        contrast_frame = tk.Frame(self.custom_params_frame, bg=LIGHT_BG, pady=5)
        contrast_frame.pack(fill=tk.X)
        tk.Label(contrast_frame, text="Contrast:", width=15, anchor=tk.W,
                bg=LIGHT_BG, fg=TEXT_COLOR, font=FONT).pack(side=tk.LEFT)
        contrast_slider = tk.Scale(contrast_frame, from_=1.0, to=2.0, variable=self.contrast,
                                  orient=tk.HORIZONTAL, bg=LIGHT_BG, fg=TEXT_COLOR,
                                  highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                                  activebackground=ACCENT_COLOR, troughcolor=DARK_BG,
                                  resolution=0.1)
        contrast_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        noise_frame = tk.Frame(self.custom_params_frame, bg=LIGHT_BG, pady=5)
        noise_frame.pack(fill=tk.X)
        tk.Label(noise_frame, text="Noise Level:", width=15, anchor=tk.W,
                bg=LIGHT_BG, fg=TEXT_COLOR, font=FONT).pack(side=tk.LEFT)
        noise_slider = tk.Scale(noise_frame, from_=0.0, to=1.0, variable=self.noise_level,
                               orient=tk.HORIZONTAL, bg=LIGHT_BG, fg=TEXT_COLOR,
                               highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                               activebackground=ACCENT_COLOR, troughcolor=DARK_BG,
                               resolution=0.1)
        noise_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        

        if self.selected_style.get() == "custom":
            self.custom_params_frame.pack(fill=tk.X, pady=(5, 0))
        

        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        progress_frame = tk.Frame(right_panel, bg=LIGHT_BG, padx=15, pady=15)
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(progress_frame, text="Progress", font=FONT, bg=LIGHT_BG, fg=TEXT_COLOR).pack(anchor=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, length=300, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(10, 5))
        
        self.progress_label = tk.Label(progress_frame, text="Ready", font=FONT, 
                                      bg=LIGHT_BG, fg=TEXT_COLOR)
        self.progress_label.pack(anchor=tk.W)
        

        logs_frame = tk.Frame(right_panel, bg=LIGHT_BG, padx=15, pady=15)
        logs_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(logs_frame, text="Logs", font=FONT, bg=LIGHT_BG, fg=TEXT_COLOR).pack(anchor=tk.W)
        
        logs_container = tk.Frame(logs_frame, bg=DARK_BG, padx=2, pady=2)
        logs_container.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.logs_box = tk.Text(logs_container, height=10, width=40, bg=DARK_BG, fg=TEXT_COLOR, 
                               font=("Consolas", 9), wrap=tk.WORD, relief=tk.FLAT)
        self.logs_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        logs_scrollbar = ttk.Scrollbar(logs_container, command=self.logs_box.yview)
        logs_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.logs_box.config(yscrollcommand=logs_scrollbar.set, state=tk.DISABLED)
        
        button_frame = tk.Frame(self, bg=DARK_BG, pady=10)
        button_frame.pack(fill=tk.X, padx=20)
        
        self.process_btn = ttk.Button(button_frame, text="Start Processing", 
                                     command=self.start_processing, style='TButton')
        self.process_btn.pack(side=tk.RIGHT, ipadx=10, ipady=5)
        
        self.reset_btn = ttk.Button(button_frame, text="Reset", 
                                   command=self.reset_form)
        self.reset_btn.pack(side=tk.RIGHT, padx=10, ipadx=10, ipady=5)
        
        self.update_log("Application started. Ready to process videos.")
    
    def select_video(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv"), ("All Files", "*.*")]
        )
        if file_path:
            self.video_path.set(file_path)
            self.update_log(f"Selected video: {os.path.basename(file_path)}")
            
            suggested_name = os.path.splitext(os.path.basename(file_path))[0]
            self.output_name.set(suggested_name)
    
    def update_log(self, log_text, level="info"):
        self.logs_box.config(state=tk.NORMAL)
        
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        if level == "error":
            tag = "error"
            self.logs_box.tag_config(tag, foreground=ERROR_COLOR)
        elif level == "success":
            tag = "success"
            self.logs_box.tag_config(tag, foreground=SUCCESS_COLOR)
        else:
            tag = "info"
            self.logs_box.tag_config(tag, foreground=TEXT_COLOR)
            
        self.logs_box.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.logs_box.tag_config("timestamp", foreground=ACCENT_COLOR)
        self.logs_box.insert(tk.END, f"{log_text}\n", tag)
        
        self.logs_box.yview(tk.END)
        self.logs_box.config(state=tk.DISABLED)
    
    def update_progress(self, value, status_text=None):
        self.progress_var.set(value)
        if status_text:
            self.progress_label.config(text=status_text)
        self.update_idletasks()
    
    def start_processing(self):
        processing_thread = threading.Thread(target=self.process_video)
        processing_thread.daemon = True
        processing_thread.start()
    

    def on_style_selected(self, event):
        """Update the style description when a style is selected"""
        self.style_desc_label.config(text=self.get_style_description())
        
        if self.selected_style.get() == "custom":
            self.custom_params_frame.pack(fill=tk.X, pady=(5, 0))
        else:
            self.custom_params_frame.pack_forget()

    def get_style_description(self):
        """Get the description for the currently selected style"""
        style_name = self.selected_style.get()
        if hasattr(core, 'get_style_description'):
            return core.get_style_description(style_name)
        
        descriptions = {
            "faith": "Low-res pixelated horror style with high contrast",
            "classic_pixel": "Clean pixel art with limited palette",
            "glitch": "Distorted pixel art with digital artifacts",
            "legacy_edge": "Original edge detection algorithm with distortion",
            "custom": "Customized pixel art style with user-defined parameters"
        }
        return descriptions.get(style_name, "No description available")

    def get_custom_params(self):
        """Get the custom style parameters as a dictionary"""
        return {
            "pixel_size": self.pixel_size.get(),
            "dithering": self.use_dithering.get(),
            "contrast": self.contrast.get(),
            "noise_level": self.noise_level.get(),
            "color_mode": "monochrome"  
        }
        
    def process_video(self):
        video_path = self.video_path.get()
        if not video_path:
            self.update_log("No video selected!", "error")
            messagebox.showerror("Error", "Please select a video file first.")
            return
            

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        

        output_name = self.output_name.get() or config["sub_directory"]
        output_dir = os.path.normpath(os.path.join(base_dir, config["output_dir"], output_name))
        nobg_dir = os.path.normpath(os.path.join(base_dir, config["output_dir"], output_name + "_nobg"))
        processed_dir = os.path.normpath(os.path.join(base_dir, config["processed_dir"], output_name))
        final_video_path = os.path.normpath(os.path.join(base_dir, config["final_video_dir"], output_name + "_final.mp4"))
    

        try:
            os.makedirs(output_dir, exist_ok=True)
            self.update_log(f"Created directory: {output_dir}")
            
            if self.export_nobg_frames.get() or self.export_processed_frames.get() or self.create_final_video.get():
                os.makedirs(nobg_dir, exist_ok=True)
                self.update_log(f"Created directory: {nobg_dir}")
            
            if self.export_processed_frames.get() or self.create_final_video.get():
                os.makedirs(processed_dir, exist_ok=True)
                self.update_log(f"Created directory: {processed_dir}")
            
            if self.create_final_video.get():
                os.makedirs(os.path.dirname(final_video_path), exist_ok=True)
                self.update_log(f"Created directory: {os.path.dirname(final_video_path)}")
        except Exception as e:
            self.update_log(f"Error creating directories: {str(e)}", "error")
            messagebox.showerror("Error", f"Failed to create required directories:\n{str(e)}")
            self.process_btn.config(state=tk.NORMAL)
            self.reset_btn.config(state=tk.NORMAL)
            return
            
        fps = self.fps.get()
        edge_threshold = [self.edge_min.get(), self.edge_max.get()]
        distortion_strength = self.distortion.get()
        
        self.process_btn.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.DISABLED)
        
        try:
            self.update_log("Starting video processing...", "info")
            
            if self.export_original_frames.get() or self.export_nobg_frames.get() or self.export_processed_frames.get() or self.create_final_video.get():
                self.update_progress(5, "Extracting frames...")
                core.extract_frames(video_path, fps, output_dir)
                self.update_log("Frames extracted successfully.", "success")
            else:
                self.update_log("No processing options selected.", "error")
                self.update_progress(0, "Ready")
                self.process_btn.config(state=tk.NORMAL)
                self.reset_btn.config(state=tk.NORMAL)
                return
            
            if self.export_nobg_frames.get() or self.export_processed_frames.get() or self.create_final_video.get():
                self.update_progress(30, "Removing background...")
                core.remove_background(output_dir, nobg_dir)
                self.update_log("Background removed successfully.", "success")
            
            if self.export_processed_frames.get() or self.create_final_video.get():
                self.update_progress(60, "Applying selected art style...")
                
                custom_params = None
                if self.selected_style.get() == "custom":
                    custom_params = self.get_custom_params()

                if hasattr(core.apply_converter_style, '__code__') and core.apply_converter_style.__code__.co_argcount > 4:
                    core.apply_converter_style(
                        nobg_dir, 
                        edge_threshold, 
                        distortion_strength, 
                        processed_dir,
                        self.selected_style.get(),
                        custom_params
                    )
                else:
                    core.apply_converter_style(nobg_dir, edge_threshold, distortion_strength, processed_dir)
                
                self.update_log(f"Applied {self.selected_style.get()} style successfully.", "success")
            
            if self.create_final_video.get():
                self.update_progress(90, "Reassembling video...")
                core.reassemble_video(processed_dir, fps, final_video_path)
                self.update_log(f"Video saved as {final_video_path}", "success")
            
            self.update_progress(100, "Completed!")
            
            completion_msg = "Processing completed!\n"
            if self.export_original_frames.get():
                completion_msg += f"- Original frames saved to: {output_dir}\n"
            if self.export_nobg_frames.get():
                completion_msg += f"- No-background frames saved to: {nobg_dir}\n"
            if self.export_processed_frames.get():
                completion_msg += f"- Processed frames saved to: {processed_dir}\n"
            if self.create_final_video.get():
                completion_msg += f"- Final video saved to: {final_video_path}"
                
            messagebox.showinfo("Success", completion_msg)
            
            if messagebox.askyesno("Open Folder", "Would you like to open the output folder?"):
                if self.create_final_video.get():
                    os.startfile(os.path.dirname(final_video_path))
                elif self.export_processed_frames.get():
                    os.startfile(processed_dir)
                elif self.export_nobg_frames.get():
                    os.startfile(nobg_dir)
                else:
                    os.startfile(output_dir)
                
        except Exception as e:
            self.update_log(f"Error during processing: {str(e)}", "error")
            messagebox.showerror("Error", f"An error occurred during processing:\n{str(e)}")
            self.update_progress(0, "Failed")
        finally:
            self.process_btn.config(state=tk.NORMAL)
            self.reset_btn.config(state=tk.NORMAL)
    
    def reset_form(self):
        self.video_path.set("")
        self.output_name.set("")
        self.fps.set(config["fps"])
        self.edge_min.set(config["edge_threshold"][0])
        self.edge_max.set(config["edge_threshold"][1])
        self.distortion.set(config["distortion_strength"])
        self.selected_style.set(config.get("default_style", "faith"))
        self.pixel_size.set(4)
        self.use_dithering.set(True)
        self.contrast.set(1.5)
        self.noise_level.set(0.2)
        self.progress_var.set(0)
        self.progress_label.config(text="Ready")
        self.update_log("Form reset to default values.")
        
        self.style_desc_label.config(text=self.get_style_description())
        
        if self.selected_style.get() != "custom":
            self.custom_params_frame.pack_forget()

if __name__ == "__main__":
    app = ConverterApp()
    app.mainloop()

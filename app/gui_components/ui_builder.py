import tkinter as tk
from tkinter import ttk
from .app_styles import DARK_BG, LIGHT_BG, ACCENT_COLOR, TEXT_COLOR, FONT, TITLE_FONT

class UIBuilder:
    """Class responsible for building the UI components"""
    
    def __init__(self, app):
        self.app = app
    
    def create_widgets(self):
        """Create all UI widgets"""
        self.create_main_frame()
        self.create_left_panel()
        self.create_right_panel()
        self.create_button_frame()
    
    def create_main_frame(self):
        """Create the main frame and title"""
        self.main_frame = ttk.Frame(self.app)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_label = tk.Label(self.main_frame, text="Video Converter", 
                              font=TITLE_FONT, bg=DARK_BG, fg=ACCENT_COLOR)
        title_label.pack(pady=(0, 20))
    
    def create_left_panel(self):
        """Create the left panel with input fields and options"""
        self.left_panel = ttk.Frame(self.main_frame)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.create_file_frame()
        self.create_output_frame()
        self.create_options_frame()
        self.create_params_frame()
        self.create_style_frame()
    
    def create_file_frame(self):
        """Create the file selection frame"""
        file_frame = tk.Frame(self.left_panel, bg=LIGHT_BG, padx=15, pady=15)
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(file_frame, text="Video File", font=FONT, bg=LIGHT_BG, fg=TEXT_COLOR).pack(anchor=tk.W)
        
        file_input_frame = tk.Frame(file_frame, bg=LIGHT_BG)
        file_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.app.video_path_entry = tk.Entry(file_input_frame, textvariable=self.app.video_path,
                                        font=FONT, bg=DARK_BG, fg=TEXT_COLOR, 
                                        insertbackground=TEXT_COLOR, relief=tk.FLAT)
        self.app.video_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5, padx=(0, 5))
        
        browse_btn = ttk.Button(file_input_frame, text="Browse", command=self.app.functions.select_video)
        browse_btn.pack(side=tk.RIGHT)
    
    def create_output_frame(self):
        """Create the output folder name frame"""
        output_frame = tk.Frame(self.left_panel, bg=LIGHT_BG, padx=15, pady=15)
        output_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(output_frame, text="Output Folder Name", font=FONT, bg=LIGHT_BG, fg=TEXT_COLOR).pack(anchor=tk.W)
        
        self.app.output_name_entry = tk.Entry(output_frame, textvariable=self.app.output_name,
                                         font=FONT, bg=DARK_BG, fg=TEXT_COLOR, 
                                         insertbackground=TEXT_COLOR, relief=tk.FLAT)
        self.app.output_name_entry.pack(fill=tk.X, expand=True, ipady=5, pady=(5, 0))
    
    def create_options_frame(self):
        """Create the processing options frame"""
        options_frame = tk.Frame(self.left_panel, bg=LIGHT_BG, padx=15, pady=15)
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(options_frame, text="Processing Options", font=FONT, bg=LIGHT_BG, fg=TEXT_COLOR).pack(anchor=tk.W)
        
        export_orig_check = ttk.Checkbutton(options_frame, text="Export Original Frames", 
                                          variable=self.app.export_original_frames, style='TCheckbutton')
        export_orig_check.pack(anchor=tk.W, pady=(5, 2))
        
        export_nobg_check = ttk.Checkbutton(options_frame, text="Export Frames with Background Removed", 
                                          variable=self.app.export_nobg_frames, style='TCheckbutton')
        export_nobg_check.pack(anchor=tk.W, pady=2)
        
        export_proc_check = ttk.Checkbutton(options_frame, text="Export Processed Frames", 
                                          variable=self.app.export_processed_frames, style='TCheckbutton')
        export_proc_check.pack(anchor=tk.W, pady=2)
        
        create_video_check = ttk.Checkbutton(options_frame, text="Create Final Video", 
                                           variable=self.app.create_final_video, style='TCheckbutton')
        create_video_check.pack(anchor=tk.W, pady=2)
    
    def create_params_frame(self):
        """Create the parameters frame with sliders"""
        params_frame = tk.Frame(self.left_panel, bg=LIGHT_BG, padx=15, pady=15)
        params_frame.pack(fill=tk.X)
        
        tk.Label(params_frame, text="Parameters", font=FONT, bg=LIGHT_BG, fg=TEXT_COLOR).pack(anchor=tk.W)
        

        fps_frame = tk.Frame(params_frame, bg=LIGHT_BG, pady=5)
        fps_frame.pack(fill=tk.X)
        
        tk.Label(fps_frame, text="FPS:", width=15, anchor=tk.W, 
                bg=LIGHT_BG, fg=TEXT_COLOR, font=FONT).pack(side=tk.LEFT)
        
        fps_slider = tk.Scale(fps_frame, from_=1, to=60, variable=self.app.fps,
                             orient=tk.HORIZONTAL, bg=LIGHT_BG, fg=TEXT_COLOR,
                             highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                             activebackground=ACCENT_COLOR, troughcolor=DARK_BG)
        fps_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        edge_min_frame = tk.Frame(params_frame, bg=LIGHT_BG, pady=5)
        edge_min_frame.pack(fill=tk.X)
        
        tk.Label(edge_min_frame, text="Min Edge Threshold:", width=15, anchor=tk.W,
                bg=LIGHT_BG, fg=TEXT_COLOR, font=FONT).pack(side=tk.LEFT)
        
        edge_min_slider = tk.Scale(edge_min_frame, from_=0, to=100, variable=self.app.edge_min,
                                  orient=tk.HORIZONTAL, bg=LIGHT_BG, fg=TEXT_COLOR,
                                  highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                                  activebackground=ACCENT_COLOR, troughcolor=DARK_BG)
        edge_min_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        edge_max_frame = tk.Frame(params_frame, bg=LIGHT_BG, pady=5)
        edge_max_frame.pack(fill=tk.X)
        
        tk.Label(edge_max_frame, text="Max Edge Threshold:", width=15, anchor=tk.W,
                bg=LIGHT_BG, fg=TEXT_COLOR, font=FONT).pack(side=tk.LEFT)
        
        edge_max_slider = tk.Scale(edge_max_frame, from_=100, to=500, variable=self.app.edge_max,
                                  orient=tk.HORIZONTAL, bg=LIGHT_BG, fg=TEXT_COLOR,
                                  highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                                  activebackground=ACCENT_COLOR, troughcolor=DARK_BG)
        edge_max_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        distortion_frame = tk.Frame(params_frame, bg=LIGHT_BG, pady=5)
        distortion_frame.pack(fill=tk.X)
        
        tk.Label(distortion_frame, text="Distortion Strength:", width=15, anchor=tk.W,
                bg=LIGHT_BG, fg=TEXT_COLOR, font=FONT).pack(side=tk.LEFT)
        
        distortion_slider = tk.Scale(distortion_frame, from_=0, to=10, variable=self.app.distortion,
                                    orient=tk.HORIZONTAL, bg=LIGHT_BG, fg=TEXT_COLOR,
                                    highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                                    activebackground=ACCENT_COLOR, troughcolor=DARK_BG,
                                    resolution=0.1)
        distortion_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
    
    def create_style_frame(self):
        """Create the art style selection frame"""
        style_frame = tk.Frame(self.left_panel, bg=LIGHT_BG, padx=15, pady=15)
        style_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Label(style_frame, text="Art Style", font=FONT, bg=LIGHT_BG, fg=TEXT_COLOR).pack(anchor=tk.W)
        
        style_combobox = ttk.Combobox(style_frame, textvariable=self.app.selected_style, 
                                     values=self.app.available_styles, state="readonly")
        style_combobox.pack(fill=tk.X, pady=(5, 10))
        style_combobox.bind("<<ComboboxSelected>>", self.app.functions.on_style_selected)

        self.app.style_desc_label = tk.Label(style_frame, text=self.app.functions.get_style_description(), 
                                       font=("Segoe UI", 8), bg=LIGHT_BG, fg=TEXT_COLOR,
                                       wraplength=300, justify=tk.LEFT)
        self.app.style_desc_label.pack(fill=tk.X, pady=(0, 10))

        self.app.custom_params_frame = tk.Frame(style_frame, bg=LIGHT_BG)
        
        pixel_frame = tk.Frame(self.app.custom_params_frame, bg=LIGHT_BG, pady=5)
        pixel_frame.pack(fill=tk.X)
        tk.Label(pixel_frame, text="Pixel Size:", width=15, anchor=tk.W,
                bg=LIGHT_BG, fg=TEXT_COLOR, font=FONT).pack(side=tk.LEFT)
        pixel_slider = tk.Scale(pixel_frame, from_=1, to=8, variable=self.app.pixel_size,
                               orient=tk.HORIZONTAL, bg=LIGHT_BG, fg=TEXT_COLOR,
                               highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                               activebackground=ACCENT_COLOR, troughcolor=DARK_BG)
        pixel_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        dither_frame = tk.Frame(self.app.custom_params_frame, bg=LIGHT_BG, pady=5)
        dither_frame.pack(fill=tk.X)
        dither_check = ttk.Checkbutton(dither_frame, text="Use Dithering", 
                                      variable=self.app.use_dithering, style='TCheckbutton')
        dither_check.pack(anchor=tk.W)
        
        contrast_frame = tk.Frame(self.app.custom_params_frame, bg=LIGHT_BG, pady=5)
        contrast_frame.pack(fill=tk.X)
        tk.Label(contrast_frame, text="Contrast:", width=15, anchor=tk.W,
                bg=LIGHT_BG, fg=TEXT_COLOR, font=FONT).pack(side=tk.LEFT)
        contrast_slider = tk.Scale(contrast_frame, from_=1.0, to=2.0, variable=self.app.contrast,
                                  orient=tk.HORIZONTAL, bg=LIGHT_BG, fg=TEXT_COLOR,
                                  highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                                  activebackground=ACCENT_COLOR, troughcolor=DARK_BG,
                                  resolution=0.1)
        contrast_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        noise_frame = tk.Frame(self.app.custom_params_frame, bg=LIGHT_BG, pady=5)
        noise_frame.pack(fill=tk.X)
        tk.Label(noise_frame, text="Noise Level:", width=15, anchor=tk.W,
                bg=LIGHT_BG, fg=TEXT_COLOR, font=FONT).pack(side=tk.LEFT)
        noise_slider = tk.Scale(noise_frame, from_=0.0, to=1.0, variable=self.app.noise_level,
                               orient=tk.HORIZONTAL, bg=LIGHT_BG, fg=TEXT_COLOR,
                               highlightthickness=0, bd=0, sliderrelief=tk.FLAT,
                               activebackground=ACCENT_COLOR, troughcolor=DARK_BG,
                               resolution=0.1)
        noise_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        if self.app.selected_style.get() == "custom":
            self.app.custom_params_frame.pack(fill=tk.X, pady=(5, 0))
    
    def create_right_panel(self):
        """Create the right panel with progress and logs"""
        self.right_panel = ttk.Frame(self.main_frame)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.create_progress_frame()
        self.create_logs_frame()
    
    def create_progress_frame(self):
        """Create the progress bar and status label"""
        progress_frame = tk.Frame(self.right_panel, bg=LIGHT_BG, padx=15, pady=15)
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(progress_frame, text="Progress", font=FONT, bg=LIGHT_BG, fg=TEXT_COLOR).pack(anchor=tk.W)
        
        self.app.progress_bar = ttk.Progressbar(progress_frame, variable=self.app.progress_var, 
                                           maximum=100, length=300, mode='determinate')
        self.app.progress_bar.pack(fill=tk.X, pady=(10, 5))
        
        self.app.progress_label = tk.Label(progress_frame, text="Ready", font=FONT, 
                                      bg=LIGHT_BG, fg=TEXT_COLOR)
        self.app.progress_label.pack(anchor=tk.W)
    
    def create_logs_frame(self):
        """Create the logs text area"""
        logs_frame = tk.Frame(self.right_panel, bg=LIGHT_BG, padx=15, pady=15)
        logs_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(logs_frame, text="Logs", font=FONT, bg=LIGHT_BG, fg=TEXT_COLOR).pack(anchor=tk.W)
        
        logs_container = tk.Frame(logs_frame, bg=DARK_BG, padx=2, pady=2)
        logs_container.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.app.logs_box = tk.Text(logs_container, height=10, width=40, bg=DARK_BG, fg=TEXT_COLOR, 
                               font=("Consolas", 9), wrap=tk.WORD, relief=tk.FLAT)
        self.app.logs_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        logs_scrollbar = ttk.Scrollbar(logs_container, command=self.app.logs_box.yview)
        logs_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.app.logs_box.config(yscrollcommand=logs_scrollbar.set, state=tk.DISABLED)
    
    def create_button_frame(self):
        """Create the bottom button frame"""
        button_frame = tk.Frame(self.app, bg=DARK_BG, pady=10)
        button_frame.pack(fill=tk.X, padx=20)
        
        self.app.process_btn = ttk.Button(button_frame, text="Start Processing", 
                                     command=self.app.functions.start_processing, style='TButton')
        self.app.process_btn.pack(side=tk.RIGHT, ipadx=10, ipady=5)
        
        self.app.reset_btn = ttk.Button(button_frame, text="Reset", 
                                   command=self.app.functions.reset_form)
        self.app.reset_btn.pack(side=tk.RIGHT, padx=10, ipadx=10, ipady=5)
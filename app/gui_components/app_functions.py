import os
import sys
import json
import shutil
import threading
from tkinter import filedialog, messagebox
from .app_styles import TEXT_COLOR, ERROR_COLOR, SUCCESS_COLOR, ACCENT_COLOR

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

with open(resource_path("config.json"), "r") as f:
    config = json.load(f)

class AppFunctions:
    """Class containing all the application functionality"""
    
    def __init__(self, app):
        self.app = app
    
    def select_video(self):
        """Open file dialog to select a video file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv"), ("All Files", "*.*")]
        )
        if file_path:
            self.app.video_path.set(file_path)
            self.update_log(f"Selected video: {os.path.basename(file_path)}")
            
            suggested_name = os.path.splitext(os.path.basename(file_path))[0]
            self.app.output_name.set(suggested_name)
    
    def update_log(self, log_text, level="info"):
        """Add a log entry to the logs box"""
        self.app.logs_box.config(state="normal")
        
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        if level == "error":
            tag = "error"
            self.app.logs_box.tag_config(tag, foreground=ERROR_COLOR)
        elif level == "success":
            tag = "success"
            self.app.logs_box.tag_config(tag, foreground=SUCCESS_COLOR)
        else:
            tag = "info"
            self.app.logs_box.tag_config(tag, foreground=TEXT_COLOR)
            
        self.app.logs_box.insert("end", f"[{timestamp}] ", "timestamp")
        self.app.logs_box.tag_config("timestamp", foreground=ACCENT_COLOR)
        self.app.logs_box.insert("end", f"{log_text}\n", tag)
        
        self.app.logs_box.yview("end")
        self.app.logs_box.config(state="disabled")
    
    def update_progress(self, value, status_text=None):
        """Update the progress bar and status text"""
        self.app.progress_var.set(value)
        if status_text:
            self.app.progress_label.config(text=status_text)
        self.app.update_idletasks()
    
    def start_processing(self):
        """Start the video processing in a separate thread"""
        processing_thread = threading.Thread(target=self.process_video)
        processing_thread.daemon = True
        processing_thread.start()
    
    def on_style_selected(self, event):
        """Update the style description when a style is selected"""
        self.app.style_desc_label.config(text=self.get_style_description())
        
        if self.app.selected_style.get() == "custom":
            self.app.custom_params_frame.pack(fill="x", pady=(5, 0))
        else:
            self.app.custom_params_frame.pack_forget()

    def get_style_description(self):
        """Get the description for the currently selected style"""
        style_name = self.app.selected_style.get()
        import core
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
            "pixel_size": self.app.pixel_size.get(),
            "dithering": self.app.use_dithering.get(),
            "contrast": self.app.contrast.get(),
            "noise_level": self.app.noise_level.get(),
            "color_mode": "monochrome"  
        }
        
    def process_video(self):
        """Process the selected video with the chosen options"""
        video_path = self.app.video_path.get()
        if not video_path:
            self.update_log("No video selected!", "error")
            messagebox.showerror("Error", "Please select a video file first.")
            return
        
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        output_name = self.app.output_name.get() or config["sub_directory"]
        output_dir = os.path.normpath(os.path.join(base_dir, config["output_dir"], output_name))
        nobg_dir = os.path.normpath(os.path.join(base_dir, config["output_dir"], output_name + "_nobg"))
        processed_dir = os.path.normpath(os.path.join(base_dir, config["processed_dir"], output_name))
        final_video_path = os.path.normpath(os.path.join(base_dir, config["final_video_dir"], output_name + "_final.mp4"))
        
        if self.app.create_final_video.get() and os.path.exists(final_video_path):
            response = messagebox.askyesnocancel(
                "File Already Exists", 
                f"The output video file already exists:\n{final_video_path}\n\nDo you want to overwrite it?\n\nYes: Overwrite\nNo: Choose a new name\nCancel: Abort processing"
            )
            
            if response is None: 
                self.update_log("Processing cancelled by user.", "info")
                return
            elif response is False: 
                new_name = filedialog.asksaveasfilename(
                    initialdir=os.path.dirname(final_video_path),
                    initialfile=os.path.basename(final_video_path),
                    defaultextension=".mp4",
                    filetypes=[("MP4 Video", "*.mp4")]
                )
                if not new_name:
                    self.update_log("Processing cancelled by user.", "info")
                    return
                final_video_path = new_name
                
                new_base_name = os.path.splitext(os.path.basename(new_name))[0]
                if new_base_name.endswith("_final"):
                    new_base_name = new_base_name[:-6]  
                self.app.output_name.set(new_base_name)
                output_name = new_base_name
                
                output_dir = os.path.normpath(os.path.join(base_dir, config["output_dir"], output_name))
                nobg_dir = os.path.normpath(os.path.join(base_dir, config["output_dir"], output_name + "_nobg"))
                processed_dir = os.path.normpath(os.path.join(base_dir, config["processed_dir"], output_name))
        
        try:
            os.makedirs(output_dir, exist_ok=True)
            self.update_log(f"Created directory: {output_dir}")
            
            if self.app.export_nobg_frames.get() or self.app.export_processed_frames.get() or self.app.create_final_video.get():
                os.makedirs(nobg_dir, exist_ok=True)
                self.update_log(f"Created directory: {nobg_dir}")
            
            if self.app.export_processed_frames.get() or self.app.create_final_video.get():
                os.makedirs(processed_dir, exist_ok=True)
                self.update_log(f"Created directory: {processed_dir}")
            
            if self.app.create_final_video.get():
                os.makedirs(os.path.dirname(final_video_path), exist_ok=True)
                self.update_log(f"Created directory: {os.path.dirname(final_video_path)}")
        except Exception as e:
            self.update_log(f"Error creating directories: {str(e)}", "error")
            messagebox.showerror("Error", f"Failed to create required directories:\n{str(e)}")
            self.app.process_btn.config(state="normal")
            self.app.reset_btn.config(state="normal")
            return
            
        fps = self.app.fps.get()
        edge_threshold = [self.app.edge_min.get(), self.app.edge_max.get()]
        distortion_strength = self.app.distortion.get()
        
        self.app.process_btn.config(state="disabled")
        self.app.reset_btn.config(state="disabled")
        
        try:
            import core
            self.update_log("Starting video processing...", "info")
            
            if self.app.export_original_frames.get() or self.app.export_nobg_frames.get() or self.app.export_processed_frames.get() or self.app.create_final_video.get():
                self.update_progress(5, "Extracting frames...")
                core.extract_frames(video_path, fps, output_dir)
                self.update_log("Frames extracted successfully.", "success")
            else:
                self.update_log("No processing options selected.", "error")
                self.update_progress(0, "Ready")
                self.app.process_btn.config(state="normal")
                self.app.reset_btn.config(state="normal")
                return
            
            if self.app.export_nobg_frames.get() or self.app.export_processed_frames.get() or self.app.create_final_video.get():
                self.update_progress(30, "Removing background...")
                core.remove_background(output_dir, nobg_dir)
                self.update_log("Background removed successfully.", "success")
            
            if self.app.export_processed_frames.get() or self.app.create_final_video.get():
                self.update_progress(60, "Applying selected art style...")
                
                custom_params = None
                if self.app.selected_style.get() == "custom":
                    custom_params = self.get_custom_params()

                if hasattr(core.apply_converter_style, '__code__') and core.apply_converter_style.__code__.co_argcount > 4:
                    core.apply_converter_style(
                        nobg_dir, 
                        edge_threshold, 
                        distortion_strength, 
                        processed_dir,
                        self.app.selected_style.get(),
                        custom_params
                    )
                else:
                    core.apply_converter_style(nobg_dir, edge_threshold, distortion_strength, processed_dir)
                
                self.update_log(f"Applied {self.app.selected_style.get()} style successfully.", "success")
            
            if self.app.create_final_video.get():
                self.update_progress(90, "Reassembling video...")
                core.reassemble_video(processed_dir, fps, final_video_path)
                self.update_log(f"Video saved as {final_video_path}", "success")
            
            self.update_progress(100, "Completed!")
            
            completion_msg = "Processing completed!\n"
            if self.app.export_original_frames.get():
                completion_msg += f"- Original frames saved to: {output_dir}\n"
            if self.app.export_nobg_frames.get():
                completion_msg += f"- No-background frames saved to: {nobg_dir}\n"
            if self.app.export_processed_frames.get():
                completion_msg += f"- Processed frames saved to: {processed_dir}\n"
            if self.app.create_final_video.get():
                completion_msg += f"- Final video saved to: {final_video_path}"
                
            messagebox.showinfo("Success", completion_msg)
            
            if not self.app.export_original_frames.get() and os.path.exists(output_dir):
                self.update_log("Cleaning up original frames...", "info")
                try:
                    shutil.rmtree(output_dir)
                    self.update_log("Original frames removed.", "success")
                except Exception as e:
                    self.update_log(f"Error removing original frames: {str(e)}", "error")
            
            if not self.app.export_nobg_frames.get() and os.path.exists(nobg_dir):
                self.update_log("Cleaning up no-background frames...", "info")
                try:
                    shutil.rmtree(nobg_dir)
                    self.update_log("No-background frames removed.", "success")
                except Exception as e:
                    self.update_log(f"Error removing no-background frames: {str(e)}", "error")
            
            if not self.app.export_processed_frames.get() and not self.app.create_final_video.get() and os.path.exists(processed_dir):
                self.update_log("Cleaning up processed frames...", "info")
                try:
                    shutil.rmtree(processed_dir)
                    self.update_log("Processed frames removed.", "success")
                except Exception as e:
                    self.update_log(f"Error removing processed frames: {str(e)}", "error")
            elif not self.app.export_processed_frames.get() and self.app.create_final_video.get() and os.path.exists(processed_dir):
                self.update_log("Cleaning up processed frames after video creation...", "info")
                try:
                    shutil.rmtree(processed_dir)
                    self.update_log("Processed frames removed.", "success")
                except Exception as e:
                    self.update_log(f"Error removing processed frames: {str(e)}", "error")
            
            if messagebox.askyesno("Open Folder", "Would you like to open the output folder?"):
                if self.app.create_final_video.get():
                    os.startfile(os.path.dirname(final_video_path))
                elif self.app.export_processed_frames.get():
                    os.startfile(processed_dir)
                elif self.app.export_nobg_frames.get():
                    os.startfile(nobg_dir)
                else:
                    os.startfile(output_dir)
                
        except Exception as e:
            self.update_log(f"Error during processing: {str(e)}", "error")
            messagebox.showerror("Error", f"An error occurred during processing:\n{str(e)}")
            self.update_progress(0, "Failed")
        finally:
            self.app.process_btn.config(state="normal")
            self.app.reset_btn.config(state="normal")
    
    def reset_form(self):
        """Reset all form fields to their default values"""
        with open(resource_path("config.json"), "r") as f:
            config = json.load(f)
            
        self.app.video_path.set("")
        self.app.output_name.set("")
        self.app.fps.set(config["fps"])
        self.app.edge_min.set(config["edge_threshold"][0])
        self.app.edge_max.set(config["edge_threshold"][1])
        self.app.distortion.set(config["distortion_strength"])
        self.app.selected_style.set(config.get("default_style", "faith"))
        self.app.pixel_size.set(4)
        self.app.use_dithering.set(True)
        self.app.contrast.set(1.5)
        self.app.noise_level.set(0.2)
        self.app.progress_var.set(0)
        self.app.progress_label.config(text="Ready")
        self.update_log("Form reset to default values.")
        
        self.app.style_desc_label.config(text=self.get_style_description())
        
        if self.app.selected_style.get() != "custom":
            self.app.custom_params_frame.pack_forget()
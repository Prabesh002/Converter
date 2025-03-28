import os
import json
import subprocess
import cv2
import numpy as np
import shutil
from PIL import Image
from rembg import remove
from art_styles import ArtStyleProcessor


with open("config.json", "r") as f:
    config = json.load(f)

art_processor = ArtStyleProcessor(config)

def extract_frames(video_path, fps, output_dir):
    command = f'ffmpeg -i "{video_path}" -vf "fps={fps}" "{output_dir}/frame_%04d.png"'
    subprocess.run(command, shell=True)

def remove_background(input_dir, output_dir):
    for file_name in os.listdir(input_dir):
        if not file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        img_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name)

        with open(img_path, "rb") as inp_file:
            img_data = inp_file.read()

        output_data = remove(img_data)

        with open(output_path, "wb") as out_file:
            out_file.write(output_data)

def apply_converter_style(input_dir, edge_threshold, distortion_strength, processed_dir, style_name=None, custom_params=None):
    """
    Apply the selected art style to images
    
    This is a wrapper around the ArtStyleProcessor that maintains compatibility
    with the existing code while adding new style options.
    """
    for file_name in os.listdir(input_dir):
        if not file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
            
        img_path = os.path.join(input_dir, file_name)
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        
        if style_name == "legacy_edge":
            result = apply_legacy_edge_detection(img, edge_threshold, distortion_strength)
        else:
            result = art_processor.process_image(img, style_name, custom_params)
        
        save_path = os.path.join(processed_dir, file_name)
        cv2.imwrite(save_path, result)

def apply_legacy_edge_detection(img, edge_threshold, distortion_strength):
    """The original edge detection algorithm, kept for compatibility"""
    if img.shape[2] == 4:
        alpha = img[:, :, 3]
        
        gray = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray, edge_threshold[0], edge_threshold[1])
        edges = cv2.bitwise_and(edges, edges, mask=alpha)
        
        rows, cols = edges.shape
        distort_map = np.random.randint(-distortion_strength, distortion_strength, (rows, cols), dtype=np.int8)
        distorted = np.clip(edges + distort_map, 0, 255)
        
        result = np.zeros((rows, cols, 4), dtype=np.uint8)
        result[:, :, 0] = distorted  
        result[:, :, 1] = distorted  
        result[:, :, 2] = distorted  
        result[:, :, 3] = alpha      
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, edge_threshold[0], edge_threshold[1])
        
        rows, cols = edges.shape
        distort_map = np.random.randint(-distortion_strength, distortion_strength, (rows, cols), dtype=np.int8)
        distorted = np.clip(edges + distort_map, 0, 255)
        
        result = np.zeros((rows, cols, 3), dtype=np.uint8)
        result[:, :, 0] = distorted  # Blue 
        result[:, :, 1] = distorted  # Green 
        result[:, :, 2] = distorted  # Red 
    
    return result

def reassemble_video(processed_dir, fps, final_video_path):
    os.makedirs(os.path.dirname(final_video_path), exist_ok=True)
    
    processed_dir = os.path.normpath(processed_dir)
    
    frame_pattern = os.path.join(processed_dir, "frame_%04d.png")
    
    frame_pattern = frame_pattern.replace('/', '\\')
    
    command = f'ffmpeg -framerate {fps} -i "{frame_pattern}" -c:v libx264 -pix_fmt yuv420p "{final_video_path}"'
    subprocess.run(command, shell=True)

def get_available_styles():
    """Return a list of available art styles"""
    styles = art_processor.get_available_styles()
    styles.append("legacy_edge")
    return styles

def get_style_description(style_name):
    """Return the description for a style"""
    if style_name == "legacy_edge":
        return "Original edge detection algorithm with distortion"
    return art_processor.get_style_description(style_name)

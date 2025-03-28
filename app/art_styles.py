import cv2
import numpy as np
import random
from PIL import Image, ImageFilter, ImageOps

class ArtStyleProcessor:
    def __init__(self, config):
        self.config = config
        self.styles = config["styles"]
        self.default_style = config["default_style"]
        
    def process_image(self, img, style_name=None, custom_params=None):
        """Process an image with the selected art style"""
        if style_name is None:
            style_name = self.default_style
            
        if style_name not in self.styles and style_name != "custom":
            print(f"Style {style_name} not found, using default style {self.default_style}")
            style_name = self.default_style
            
        if style_name == "custom" and custom_params:
            style_params = custom_params
        else:
            style_params = self.styles[style_name]
            
        if len(img.shape) == 3 and img.shape[2] == 4:
            has_alpha = True
            alpha = img[:, :, 3].copy()
            rgb_img = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_img)
        else:
            has_alpha = False
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_img)
            
        if style_name == "faith" or (style_name == "custom" and style_params.get("color_mode") == "monochrome"):
            processed_img = self._apply_faith_style(pil_img, style_params)
        elif style_name == "classic_pixel" or (style_name == "custom" and style_params.get("color_mode") == "limited_palette"):
            processed_img = self._apply_classic_pixel_style(pil_img, style_params)
        elif style_name == "glitch" or (style_name == "custom" and style_params.get("color_mode") == "rgb_shift"):
            processed_img = self._apply_glitch_style(pil_img, style_params)
        else:
            processed_img = self._apply_faith_style(pil_img, self.styles["faith"])
            
        result = np.array(processed_img)
        result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
        
        if has_alpha:
            result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
            result[:, :, 3] = alpha
            
        return result
        
    def _apply_faith_style(self, img, params):
        """Apply Faith: The Unholy Trinity style to the image"""
        pixel_size = params.get("pixel_size", 4)
        contrast = params.get("contrast", 1.5)
        noise_level = params.get("noise_level", 0.2)
        use_dithering = params.get("dithering", True)
        
        width, height = img.size
        small_size = (width // pixel_size, height // pixel_size)
        pixelated = img.resize(small_size, Image.NEAREST)
        
        pixelated = ImageOps.grayscale(pixelated)
        
        enhancer = ImageOps.autocontrast(pixelated, cutoff=10)
        
        if use_dithering:
            result = pixelated.convert('1', dither=Image.FLOYDSTEINBERG)
        else:
            result = pixelated.point(lambda x: 0 if x < 128 else 255, '1')
        
        result = result.convert('RGB')
        
        result = result.resize((width, height), Image.NEAREST)
        
        if noise_level > 0:
            noise = np.random.randint(0, int(noise_level * 255), (height, width, 3), dtype=np.uint8)
            result_array = np.array(result)
            result_array = cv2.add(result_array, noise)
            result = Image.fromarray(result_array)
            
        return result
        
    def _apply_classic_pixel_style(self, img, params):
        """Apply classic pixel art style with limited color palette"""
        pixel_size = params.get("pixel_size", 3)
        contrast = params.get("contrast", 1.2)
        
        width, height = img.size
        small_size = (width // pixel_size, height // pixel_size)
        pixelated = img.resize(small_size, Image.NEAREST)
        
        pixelated = ImageOps.autocontrast(pixelated, cutoff=5)
        
        pixelated = pixelated.quantize(16).convert('RGB')
        
        result = pixelated.resize((width, height), Image.NEAREST)
        
        return result
        
    def _apply_glitch_style(self, img, params):
        """Apply glitch art style with digital artifacts"""
        pixel_size = params.get("pixel_size", 2)
        noise_level = params.get("noise_level", 0.5)
        
        width, height = img.size
        small_size = (width // pixel_size, height // pixel_size)
        pixelated = img.resize(small_size, Image.NEAREST)
        
        r, g, b = pixelated.split()

        shift = int(width * 0.02)
        r = ImageOps.crop(r, (shift, 0, 0, 0))
        r = ImageOps.expand(r, (0, 0, shift, 0), fill=0)
        
        b = ImageOps.crop(b, (0, 0, shift, 0))
        b = ImageOps.expand(b, (shift, 0, 0, 0), fill=0)

        result = Image.merge("RGB", (r, g, b))
        
        if noise_level > 0:
            for _ in range(int(10 * noise_level)):
                block_x = random.randint(0, small_size[0] - 3)
                block_y = random.randint(0, small_size[1] - 3)
                block_w = random.randint(1, 6)
                block_h = random.randint(1, 6)
                
                block = result.crop((block_x, block_y, block_x + block_w, block_y + block_h))
                shift_x = random.randint(-3, 3)
                result.paste(block, (block_x + shift_x, block_y))

        result = result.resize((width, height), Image.NEAREST)
        
        return result

    def get_available_styles(self):
        """Return a list of available style names"""
        return list(self.styles.keys())
        
    def get_style_description(self, style_name):
        """Return the description for a style"""
        if style_name in self.styles:
            return self.styles[style_name].get("description", "No description available")
        return "Style not found"
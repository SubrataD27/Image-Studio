import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from rembg import remove
from PIL import Image, ImageEnhance, ImageFilter
import io
import cv2
import numpy as np

UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.secret_key = 'supersecretkey'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_background(image_path):
    """Remove background from image"""
    with open(image_path, 'rb') as inp:
        input_data = inp.read()
    output_data = remove(input_data)
    img = Image.open(io.BytesIO(output_data))
    return img

def compress_image(image_path, quality=85):
    """Compress image with specified quality"""
    img = Image.open(image_path)
    # Convert to RGB if necessary for JPEG compression
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGB')
    
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)
    return Image.open(output)

def resize_image(image_path, width=None, height=None, maintain_aspect=True):
    """Resize image to specified dimensions"""
    img = Image.open(image_path)
    original_width, original_height = img.size
    
    if maintain_aspect:
        if width and not height:
            height = int((width / original_width) * original_height)
        elif height and not width:
            width = int((height / original_height) * original_width)
        elif width and height:
            # Maintain aspect ratio and fit within bounds
            ratio = min(width / original_width, height / original_height)
            width = int(original_width * ratio)
            height = int(original_height * ratio)
    
    return img.resize((width, height), Image.Resampling.LANCZOS)

def change_background_color(image_path, bg_color='white'):
    """Change background color of image"""
    # First remove the background
    img = remove_background(image_path)
    
    # Create new image with specified background color
    if bg_color == 'transparent':
        return img
    
    # Color mapping
    color_map = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'purple': (128, 0, 128),
        'pink': (255, 192, 203)
    }
    
    bg_rgb = color_map.get(bg_color, (255, 255, 255))
    background = Image.new('RGB', img.size, bg_rgb)
    
    if img.mode == 'RGBA':
        background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
    else:
        background.paste(img)
    
    return background

def enhance_image(image_path, brightness=1.0, contrast=1.0, saturation=1.0, sharpness=1.0):
    """Enhance image with various filters"""
    img = Image.open(image_path)
    
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)
    
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contrast)
    
    if saturation != 1.0:
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(saturation)
    
    if sharpness != 1.0:
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(sharpness)
    
    return img

def apply_blur_effect(image_path, blur_radius=2):
    """Apply blur effect to image"""
    img = Image.open(image_path)
    return img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Get the operation type
            operation = request.form.get('operation', 'remove_bg')
            
            try:
                if operation == 'remove_bg':
                    result_img = remove_background(filepath)
                    result_filename = f"{os.path.splitext(filename)[0]}_no_bg.png"
                    
                elif operation == 'compress':
                    quality = int(request.form.get('quality', 85))
                    result_img = compress_image(filepath, quality)
                    result_filename = f"{os.path.splitext(filename)[0]}_compressed.jpg"
                    
                elif operation == 'resize':
                    width = request.form.get('width')
                    height = request.form.get('height')
                    width = int(width) if width else None
                    height = int(height) if height else None
                    result_img = resize_image(filepath, width, height)
                    result_filename = f"{os.path.splitext(filename)[0]}_resized.png"
                    
                elif operation == 'change_bg':
                    bg_color = request.form.get('bg_color', 'white')
                    result_img = change_background_color(filepath, bg_color)
                    ext = '.png' if bg_color == 'transparent' else '.jpg'
                    result_filename = f"{os.path.splitext(filename)[0]}_bg_{bg_color}{ext}"
                    
                elif operation == 'enhance':
                    brightness = float(request.form.get('brightness', 1.0))
                    contrast = float(request.form.get('contrast', 1.0))
                    saturation = float(request.form.get('saturation', 1.0))
                    sharpness = float(request.form.get('sharpness', 1.0))
                    result_img = enhance_image(filepath, brightness, contrast, saturation, sharpness)
                    result_filename = f"{os.path.splitext(filename)[0]}_enhanced.png"
                    
                elif operation == 'blur':
                    blur_radius = float(request.form.get('blur_radius', 2))
                    result_img = apply_blur_effect(filepath, blur_radius)
                    result_filename = f"{os.path.splitext(filename)[0]}_blurred.png"
                
                # Save the result
                result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
                
                # Determine format based on file extension
                if result_filename.endswith('.jpg'):
                    if result_img.mode in ('RGBA', 'LA', 'P'):
                        result_img = result_img.convert('RGB')
                    result_img.save(result_path, format='JPEG', quality=95)
                else:
                    result_img.save(result_path, format='PNG')
                
                return render_template('index.html', 
                                     original_image=filepath, 
                                     result_image=result_path,
                                     operation=operation)
                                     
            except Exception as e:
                flash(f'Error processing image: {str(e)}')
                return redirect(request.url)
                
    return render_template('index_custom.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)

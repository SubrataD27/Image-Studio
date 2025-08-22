import os
import time
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from PIL import Image, ImageEnhance, ImageFilter
import io

UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.secret_key = 'supersecretkey'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Add port configuration for development server
port = int(os.environ.get('PORT', 10000))

def cleanup_old_files():
    """Clean up files older than 1 hour"""
    current_time = time.time()
    for folder in [UPLOAD_FOLDER, RESULT_FOLDER]:
        try:
            for filename in os.listdir(folder):
                filepath = os.path.join(folder, filename)
                # If file is older than 1 hour, delete it
                if os.path.getmtime(filepath) < current_time - 3600:
                    try:
                        os.remove(filepath)
                    except:
                        pass
        except:
            pass

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_background(image_path):
    """Mock background removal - just return original for testing"""
    img = Image.open(image_path)
    return img.convert('RGBA')

def compress_image(image_path, quality=85):
    """Compress image with specified quality"""
    img = Image.open(image_path)
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
            ratio = min(width / original_width, height / original_height)
            width = int(original_width * ratio)
            height = int(original_height * ratio)
    
    return img.resize((width, height), Image.Resampling.LANCZOS)

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
    cleanup_old_files()
    
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
                
                result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
                
                if result_filename.endswith('.jpg'):
                    if result_img.mode in ('RGBA', 'LA', 'P'):
                        result_img = result_img.convert('RGB')
                    result_img.save(result_path, format='JPEG', quality=95)
                else:
                    result_img.save(result_path, format='PNG')
                
                try:
                    os.remove(filepath)
                except:
                    pass
                
                return render_template('index_custom.html', 
                                     result_image=result_path,
                                     operation=operation,
                                     success=True)
                                     
            except Exception as e:
                flash(f'Error processing image: {str(e)}')
                return redirect(request.url)
                
    return render_template('index_custom.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

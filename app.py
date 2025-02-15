from flask import Flask, render_template, request, send_file
from PIL import Image
import io
import random
import numpy as np

app = Flask(__name__)

def apply_glitch_effect(img, intensity):
    # Convert image to numpy array
    img_array = np.array(img)
    
    # Scale number of effects based on intensity (1-10)
    num_effects = int(intensity * 1.5)  # 1-15 effects
    
    # Random transformations
    for _ in range(num_effects):
        effect = random.choice(['shift', 'corrupt', 'color'])
        
        if effect == 'shift':
            # Scale shift amount by intensity
            shift = random.randint(10, int(10 + intensity * 8))
            direction = random.choice(['horizontal', 'vertical'])
            if direction == 'horizontal':
                img_array = np.roll(img_array, shift, axis=1)
            else:
                img_array = np.roll(img_array, shift, axis=0)
                
        elif effect == 'corrupt':
            # Scale corruption probability by intensity
            corruption_prob = 0.02 * intensity
            mask = np.random.random(img_array.shape[:2]) < corruption_prob
            img_array[mask] = np.random.randint(0, 255, size=3)
            
        elif effect == 'color':
            # Scale color shift by intensity
            shift_amount = random.randint(-10 * intensity, 10 * intensity)
            channel = random.randint(0, 2)
            img_array[:, :, channel] = np.roll(img_array[:, :, channel], shift_amount)
    
    return Image.fromarray(img_array)

def jpeg_compression_hell(img, intensity):
    # Scale number of compressions by intensity
    num_compressions = random.randint(2, int(intensity * 2))
    min_quality = max(1, 20 - intensity * 2)  # Lower quality for higher intensity
    
    for _ in range(num_compressions):
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=random.randint(min_quality, 30))
        buffer.seek(0)
        img = Image.open(buffer)
    return img

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded'
        
        file = request.files['file']
        if file.filename == '':
            return 'No file selected'
        
        # Get intensity value from form
        intensity = float(request.form.get('intensity', 5))
        
        # Process the image
        img = Image.open(file)
        img = img.convert('RGB')
        
        effect_type = request.form.get('effect', 'glitch')
        
        if effect_type == 'glitch':
            processed_img = apply_glitch_effect(img, intensity)
        else:  # jpeg_hell
            processed_img = jpeg_compression_hell(img, intensity)
        
        # Save to bytes
        img_io = io.BytesIO()
        processed_img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True) 

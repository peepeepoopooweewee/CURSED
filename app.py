from flask import Flask, render_template, request, send_file
from PIL import Image
import io
import random
import numpy as np

app = Flask(__name__)

def apply_glitch_effect(img):
    # Convert image to numpy array
    img_array = np.array(img)
    
    # Random transformations
    for _ in range(random.randint(3, 8)):
        # Randomly choose effect
        effect = random.choice(['shift', 'corrupt', 'color'])
        
        if effect == 'shift':
            # Randomly shift image sections
            shift = random.randint(10, 50)
            direction = random.choice(['horizontal', 'vertical'])
            if direction == 'horizontal':
                img_array = np.roll(img_array, shift, axis=1)
            else:
                img_array = np.roll(img_array, shift, axis=0)
                
        elif effect == 'corrupt':
            # Corrupt random pixels
            mask = np.random.random(img_array.shape[:2]) < 0.1
            img_array[mask] = np.random.randint(0, 255, size=3)
            
        elif effect == 'color':
            # Color channel manipulation
            channel = random.randint(0, 2)
            img_array[:, :, channel] = np.roll(img_array[:, :, channel], 
                                             random.randint(-50, 50))
    
    return Image.fromarray(img_array)

def jpeg_compression_hell(img):
    # Save and reload the image multiple times with low quality
    for _ in range(random.randint(5, 15)):
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=random.randint(1, 10))
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
        
        # Process the image
        img = Image.open(file)
        img = img.convert('RGB')  # Convert to RGB mode
        
        effect_type = request.form.get('effect', 'glitch')
        
        if effect_type == 'glitch':
            processed_img = apply_glitch_effect(img)
        else:  # jpeg_hell
            processed_img = jpeg_compression_hell(img)
        
        # Save to bytes
        img_io = io.BytesIO()
        processed_img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True) 
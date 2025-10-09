import numpy as np
from PIL import Image
import os

def create_sample_images():
    """Create sample polarization images for testing without OpenCV"""
    print("Creating sample polarization images...")
    
    # Create output directory
    os.makedirs('sample_images', exist_ok=True)
    
    height, width = 400, 400
    
    # Create base pattern
    x, y = np.meshgrid(np.linspace(-2, 2, width), np.linspace(-2, 2, height))
    base_pattern = np.sin(3 * np.pi * np.sqrt(x**2 + y**2))
    
    # Create 4 polarization images with different characteristics
    angles = [0, 45, 90, 135]
    
    for angle in angles:
        # Simulate different polarization responses
        img = base_pattern * np.cos(np.deg2rad(angle)) + 0.3 * base_pattern * np.sin(np.deg2rad(angle))
        
        # Add some noise and variations
        noise = np.random.normal(0, 0.1, (height, width))
        img = img + noise
        
        # Normalize to 0-255
        img = (img - img.min()) / (img.max() - img.min()) * 255
        img = img.astype(np.uint8)
        
        # Save image using PIL instead of OpenCV
        filename = f'sample_images/polarization_{angle}deg.png'
        Image.fromarray(img).save(filename)
        print(f"Created: {filename}")
    
    print("Sample images created in 'sample_images' folder!")
    print("You can use these for testing the application.")

if __name__ == "__main__":
    create_sample_images()
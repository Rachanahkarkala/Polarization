import numpy as np
from PIL import Image
import os
import sys

def create_verification_samples():
    """Create sample polarization images with clear patterns for verification"""
    print("🚀 Starting verification sample creation...")
    
    # Create output directory
    output_dir = 'verification_samples'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Created directory: {output_dir}")
    else:
        print(f"📁 Directory already exists: {output_dir}")
    
    height, width = 400, 400
    print(f"📐 Creating images of size: {width}x{height}")
    
    # Create coordinate grids
    x, y = np.meshgrid(np.linspace(0, 4*np.pi, width), np.linspace(0, 4*np.pi, height))
    print("📊 Generated coordinate grids")
    
    # Different patterns for each polarization angle
    patterns = {
        0: np.sin(2*x) * np.cos(2*y),      # Horizontal stripes
        45: np.sin(x + y) * np.cos(x - y), # Diagonal  
        90: np.cos(2*x) * np.sin(2*y),     # Vertical stripes
        135: np.cos(x + y) * np.sin(x - y) # Opposite diagonal
    }
    
    print("🎨 Generating polarization images...")
    
    # Create 4 polarization images
    for angle, base_pattern in patterns.items():
        print(f"🖼️  Processing {angle}° image...")
        
        # Add polarization-specific variations
        if angle == 0:    # 0° - strongest horizontal response
            img = base_pattern * 0.8 + 0.2 * np.sin(3*x)
        elif angle == 45: # 45° - diagonal response
            img = base_pattern * 0.7 + 0.3 * np.sin(x + y)
        elif angle == 90: # 90° - strongest vertical response  
            img = base_pattern * 0.8 + 0.2 * np.cos(3*y)
        else: # 135° - opposite diagonal
            img = base_pattern * 0.7 + 0.3 * np.cos(x + y)
        
        # Add some realistic noise
        noise = np.random.normal(0, 0.05, (height, width))
        img = img + noise
        
        # Normalize to 0-255
        img = (img - img.min()) / (img.max() - img.min()) * 200 + 28
        img = np.clip(img, 0, 255).astype(np.uint8)
        
        # Save image
        filename = f'{output_dir}/polarization_{angle}deg.png'
        Image.fromarray(img).save(filename)
        print(f"✅ Saved: {filename}")
        
        # Show some image stats
        print(f"   📈 Image stats - Min: {img.min()}, Max: {img.max()}, Mean: {img.mean():.1f}")

def create_simple_checkerboard():
    """Create a simple checkerboard pattern for basic verification"""
    print("\n🏁 Creating checkerboard patterns...")
    
    height, width = 400, 400
    checker_size = 40
    
    # Create checkerboard pattern
    checkerboard = np.zeros((height, width))
    for i in range(0, height, checker_size):
        for j in range(0, width, checker_size):
            if (i // checker_size + j // checker_size) % 2 == 0:
                checkerboard[i:i+checker_size, j:j+checker_size] = 200
            else:
                checkerboard[i:i+checker_size, j:j+checker_size] = 50
    
    print("⚫⚪ Checkerboard base created")
    
    # Save with variations
    angles = [0, 45, 90, 135]
    for angle in angles:
        variation = np.random.normal(0, 10, (height, width))
        img = checkerboard + variation
        img = np.clip(img, 0, 255).astype(np.uint8)
        
        filename = f'verification_samples/checkerboard_{angle}deg.png'
        Image.fromarray(img).save(filename)
        print(f"✅ Saved: {filename}")

if __name__ == "__main__":
    print("=" * 60)
    print("🎯 POLARIZATION VERIFICATION SAMPLE GENERATOR")
    print("=" * 60)
    
    try:
        create_verification_samples()
        create_simple_checkerboard()
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Verification samples created!")
        print("=" * 60)
        print("\n📋 FILES CREATED:")
        print("├── polarization_0deg.png")
        print("├── polarization_45deg.png") 
        print("├── polarization_90deg.png")
        print("├── polarization_135deg.png")
        print("├── checkerboard_0deg.png")
        print("├── checkerboard_45deg.png")
        print("├── checkerboard_90deg.png")
        print("└── checkerboard_135deg.png")
        
        print("\n🔍 HOW TO TEST YOUR WEBSITE:")
        print("1. Run: streamlit run app.py")
        print("2. Go to: http://localhost:8501")
        print("3. Click 'Single Image Analysis'")
        print("4. Upload the 4 polarization_*deg.png files")
        print("5. Check if you see colorful heatmaps and numbers!")
        
        print("\n✅ EXPECTED RESULTS:")
        print("• DOP: 0.4 - 0.7")
        print("• Orientation: Various angles") 
        print("• 6 different colorful plots")
        print("• No error messages!")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("💡 TROUBLESHOOTING:")
        print("• Check if PIL (Pillow) is installed: pip install Pillow")
        print("• Check if numpy is installed: pip install numpy")
        input("Press Enter to exit...")
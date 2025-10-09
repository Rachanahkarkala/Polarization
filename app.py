import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import time

# Import our enhanced components
from utils.shaders import get_shader_background
from utils.canvas_flame import get_canvas_flame
from utils.polarization import PolarizationProcessor
from utils.visualization import PolarizationVisualizer
from utils.file_handling import FileExporter

# Page configuration - MUST BE FIRST
st.set_page_config(
    page_title="PolarVision - Polarization Analysis",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply WebGL shader background
st.markdown(get_shader_background(), unsafe_allow_html=True)
# Add flame-like canvas background
st.markdown(get_canvas_flame(), unsafe_allow_html=True)


def main():
    # Main header with animated elements
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 3.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2, #00ff88);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;'>
                🌊 PolarVision
            </h1>
            <p style='font-size: 1.2rem; color: rgba(255,255,255,0.8); margin-top: 0;'>
                Advanced Polarization Image Analysis with Real-time Processing
            </p>
            <div style='display: flex; justify-content: center; align-items: center; gap: 10px; margin-top: 1rem;'>
                <span style='
                    display: inline-block;
                    width: 16px;
                    height: 16px;
                    background-color: #00ff88;
                    border-radius: 50%;
                    box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7);
                    animation: pulse-green 3s infinite;
                '></span>
                <span style='color: rgba(255,255,255,0.7);'>Live Processing Ready</span>
            </div>
        </div>
        
        <style>
            @keyframes pulse-green {
                0% {
                    transform: scale(0.95);
                    box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7);
                }
                
                70% {
                    transform: scale(1.1);
                    box-shadow: 0 0 0 10px rgba(0, 255, 136, 0);
                }
                
                100% {
                    transform: scale(0.95);
                    box-shadow: 0 0 0 0 rgba(0, 255, 136, 0);
                }
            }
        </style>
        """, unsafe_allow_html=True)
    
    # Sidebar with enhanced design
    with st.sidebar:
        st.markdown("""
        <div class='glass-card' style='padding: 1.5rem;'>
            <h3 style='color: white; margin-bottom: 1.5rem;'>🔮 Navigation</h3>
        """, unsafe_allow_html=True)
        
        app_mode = st.radio(
            "Choose Analysis Mode",
            ["🎯 Single Image Analysis", "🔄 Dual Image Analysis", "🚀 Demo Mode", "📚 Learn"],
            key="nav"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Quick stats
        st.markdown("""
        <div class='glass-card' style='padding: 1rem; margin-top: 1rem;'>
            <h4 style='color: white; margin-bottom: 1rem;'>📊 System Status</h4>
            <div style='display: flex; justify-content: space-between; color: rgba(255,255,255,0.8);'>
                <span>Processing:</span>
                <span style='color: #00ff88;'>✅ Ready</span>
            </div>
            <div style='display: flex; justify-content: space-between; color: rgba(255,255,255,0.8); margin-top: 0.5rem;'>
                <span>WebGL:</span>
                <span style='color: #00ff88;'>✅ Active</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Route to appropriate page
    if "Single Image Analysis" in app_mode:
        single_image_analysis()
    elif "Dual Image Analysis" in app_mode:
        dual_image_analysis()
    elif "Demo Mode" in app_mode:
        demo_mode()
    else:
        learn_page()

def single_image_analysis():
    st.markdown("""
    <div class='glass-card'>
        <h2 style='color: white; margin-bottom: 1rem;'>🎯 Single Image Analysis</h2>
        <p style='color: rgba(255,255,255,0.8);'>
            Upload 4 polarization images taken at different angles (0°, 45°, 90°, 135°) to perform 
            comprehensive polarization analysis using Stokes parameters.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Information bubble
    st.markdown("""
    <div class='info-bubble'>
        <strong>💡 How it works:</strong> The Stokes parameters (S₀, S₁, S₂) are calculated from the four input images, 
        revealing how light waves are organized in space. This helps uncover material properties invisible to regular cameras.
    </div>
    """, unsafe_allow_html=True)
    
    # File upload with enhanced UI
    st.markdown("""
    <div class='upload-area'>
        <h3 style='color: white; margin-bottom: 1rem;'>📁 Upload Polarization Images</h3>
        <p style='color: rgba(255,255,255,0.7);'>Drag and drop 4 images taken at 0°, 45°, 90°, and 135° angles</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "",
        type=['png', 'jpg', 'jpeg', 'tiff', 'bmp'],
        accept_multiple_files=True,
        key="single_upload",
        label_visibility="collapsed"
    )
    
    if uploaded_files and len(uploaded_files) == 4:
        with st.spinner("🔮 Processing images with Stokes parameter analysis..."):
            # Add processing animation
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            images = []
            file_names = []
            
            for file in uploaded_files:
                img = Image.open(file).convert('L')
                images.append(np.array(img, dtype=np.float32))
                file_names.append(file.name)
            
            processor = PolarizationProcessor()
            visualizer = PolarizationVisualizer()
            exporter = FileExporter()
            
            stokes = processor.compute_stokes_single(images)
            metrics = processor.compute_polarization_metrics(stokes)
            
            display_enhanced_results(images, metrics, file_names, visualizer, exporter)
            
    elif uploaded_files and len(uploaded_files) != 4:
        st.error("❌ Please upload exactly 4 images for comprehensive polarization analysis")

def dual_image_analysis():
    st.markdown("""
    <div class='glass-card'>
        <h2 style='color: white; margin-bottom: 1rem;'>🔄 Dual Image Analysis</h2>
        <p style='color: rgba(255,255,255,0.8);'>
            Quick analysis using two polarization images (0° and 90°). Perfect for rapid material inspection.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='upload-area' style='padding: 2rem;'>
            <h4 style='color: white;'>0° Image</h4>
            <p style='color: rgba(255,255,255,0.7); font-size: 0.9rem;'>Horizontal polarization</p>
        </div>
        """, unsafe_allow_html=True)
        I0_file = st.file_uploader("Upload 0° image", type=['png', 'jpg', 'jpeg'], key="I0", label_visibility="collapsed")
    
    with col2:
        st.markdown("""
        <div class='upload-area' style='padding: 2rem;'>
            <h4 style='color: white;'>90° Image</h4>
            <p style='color: rgba(255,255,255,0.7); font-size: 0.9rem;'>Vertical polarization</p>
        </div>
        """, unsafe_allow_html=True)
        I90_file = st.file_uploader("Upload 90° image", type=['png', 'jpg', 'jpeg'], key="I90", label_visibility="collapsed")
    
    if I0_file and I90_file:
        with st.spinner("🔄 Processing dual-image analysis..."):
            I0 = Image.open(I0_file).convert('L')
            I0 = np.array(I0, dtype=np.float32)
            
            I90 = Image.open(I90_file).convert('L')
            I90 = np.array(I90, dtype=np.float32)
            
            processor = PolarizationProcessor()
            visualizer = PolarizationVisualizer()
            
            stokes = processor.compute_stokes_dual(I0, I90)
            metrics = processor.compute_polarization_metrics(stokes)
            
            # Enhanced metrics display
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class='metric-card pulse-glow'>
                    <h3 style='color: #00ff88; margin: 0;'>{np.mean(metrics['dop']):.3f}</h3>
                    <p style='color: rgba(255,255,255,0.8); margin: 0;'>Degree of Polarization</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class='metric-card'>
                    <h3 style='color: #667eea; margin: 0;'>{np.mean(metrics['orientation_angle']):.1f}°</h3>
                    <p style='color: rgba(255,255,255,0.8); margin: 0;'>Avg Orientation</p>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class='metric-card'>
                    <h3 style='color: #764ba2; margin: 0;'>{I0.shape[1]}x{I0.shape[0]}</h3>
                    <p style='color: rgba(255,255,255,0.8); margin: 0;'>Image Size</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.plotly_chart(
                visualizer.create_heatmap(metrics['dop'], '🎯 Degree of Polarization (DOP)'),
                use_container_width=True
            )

def demo_mode():
    st.markdown("""
    <div class='glass-card'>
        <h2 style='color: white; margin-bottom: 1rem;'>🚀 Interactive Demo</h2>
        <p style='color: rgba(255,255,255,0.8);'>
            Experience the power of polarization analysis with our pre-loaded sample data. 
            See how different materials affect light polarization in real-time.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎮 Generate Sample Analysis", use_container_width=True):
            with st.spinner("✨ Creating magical polarization data..."):
                # Create sample data
                height, width = 300, 300
                x, y = np.meshgrid(np.linspace(-2, 2, width), np.linspace(-2, 2, height))
                
                S0 = np.ones((height, width))
                S1 = np.sin(3 * np.pi * x) * np.cos(3 * np.pi * y)
                S2 = np.cos(3 * np.pi * x) * np.sin(3 * np.pi * y)
                
                stokes = np.stack([S0, S1, S2], axis=-1)
                metrics = PolarizationProcessor.compute_polarization_metrics(stokes)
                
                visualizer = PolarizationVisualizer()
                st.plotly_chart(
                    visualizer.create_comprehensive_plots(metrics),
                    use_container_width=True
                )
    
    with col2:
        if st.button("📁 Load Sample Images", use_container_width=True):
            if os.path.exists('verification_samples'):
                st.success("✅ Sample images loaded! Switch to Single Image Analysis to use them.")
            else:
                st.warning("📝 Please run create_verification_samples.py first")

def learn_page():
    st.markdown("""
    <div class='glass-card'>
        <h2 style='color: white; margin-bottom: 1rem;'>📚 Understanding Polarization Analysis</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h3 style='color: white;'>🌊 What is Light Polarization?</h3>
            <p style='color: rgba(255,255,255,0.8);'>
                Light waves normally vibrate in all directions. Polarized light vibrates primarily in one direction, 
                like waves in a rope being shaken up and down.
            </p>
        </div>
        
        <div class='glass-card' style='margin-top: 1rem;'>
            <h3 style='color: white;'>🔍 Stokes Parameters</h3>
            <p style='color: rgba(255,255,255,0.8);'>
                <strong>S₀</strong> - Total light intensity<br>
                <strong>S₁</strong> - Horizontal vs vertical polarization<br>
                <strong>S₂</strong> - Diagonal polarization<br>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='glass-card'>
            <h3 style='color: white;'>🎯 Degree of Polarization (DOP)</h3>
            <p style='color: rgba(255,255,255,0.8);'>
                Measures how much of the light is polarized vs unpolarized. 
                Ranges from 0 (completely unpolarized) to 1 (fully polarized).
            </p>
        </div>
        
        <div class='glass-card' style='margin-top: 1rem;'>
            <h3 style='color: white;'>💫 Real-world Applications</h3>
            <p style='color: rgba(255,255,255,0.8);'>
                • Material science & quality control<br>
                • Medical imaging & diagnostics<br>
                • Remote sensing & environmental monitoring<br>
                • Computer vision & autonomous vehicles<br>
            </p>
        </div>
        """, unsafe_allow_html=True)

def display_enhanced_results(images, metrics, file_names, visualizer, exporter):
    # Success message with animation
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0,255,136,0.2), rgba(102,126,234,0.2)); 
                border: 1px solid rgba(0,255,136,0.3); border-radius: 15px; padding: 2rem; text-align: center;'>
        <h2 style='color: #00ff88; margin: 0;'>✅ Analysis Complete!</h2>
        <p style='color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0;'>Polarization metrics successfully calculated</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced metrics display
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card pulse-glow'>
            <h2 style='color: #00ff88; margin: 0; font-size: 2rem;'>{np.mean(metrics['dop']):.3f}</h2>
            <p style='color: rgba(255,255,255,0.8); margin: 0;'>Degree of Polarization</p>
            <div style='height: 4px; background: rgba(255,255,255,0.2); border-radius: 2px; margin-top: 0.5rem;'>
                <div style='height: 100%; background: #00ff88; border-radius: 2px; width: {np.mean(metrics['dop'])*100}%;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h2 style='color: #667eea; margin: 0; font-size: 2rem;'>{np.mean(metrics['orientation_angle']):.1f}°</h2>
            <p style='color: rgba(255,255,255,0.8); margin: 0;'>Orientation Angle</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <h2 style='color: #764ba2; margin: 0; font-size: 2rem;'>{np.mean(metrics['ellipticity_angle']):.1f}°</h2>
            <p style='color: rgba(255,255,255,0.8); margin: 0;'>Ellipticity Angle</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <h2 style='color: #ff6b6b; margin: 0; font-size: 2rem;'>{images[0].shape[1]}x{images[0].shape[0]}</h2>
            <p style='color: rgba(255,255,255,0.8); margin: 0;'>Image Resolution</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Comprehensive visualization
    st.markdown("""
    <div class='glass-card' style='margin-top: 2rem;'>
        <h2 style='color: white; margin-bottom: 1rem;'>📊 Polarization Analysis Dashboard</h2>
        <p style='color: rgba(255,255,255,0.7);'>
            Interactive visualization of all polarization parameters. Hover over plots for detailed values.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.plotly_chart(
        visualizer.create_comprehensive_plots(metrics),
        use_container_width=True
    )
    
    # Statistical summary
    st.markdown("""
    <div class='glass-card'>
        <h2 style='color: white; margin-bottom: 1rem;'>📈 Statistical Summary</h2>
    </div>
    """, unsafe_allow_html=True)
    
    stats_df = exporter.create_summary_statistics(metrics)
    st.dataframe(stats_df.style.background_gradient(cmap='Blues'), use_container_width=True)
    
    # Export options
    st.markdown("""
    <div class='glass-card'>
        <h2 style='color: white; margin-bottom: 1rem;'>💾 Export Results</h2>
        <p style='color: rgba(255,255,255,0.7);'>
            Download your analysis results for further processing or reporting.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export to Excel", use_container_width=True):
            filename = exporter.export_to_excel(metrics)
            st.success(f"✅ Results exported to {filename}")
    
    with col2:
        csv_data = stats_df.to_csv(index=False)
        st.download_button(
            label="📄 Download Statistics CSV",
            data=csv_data,
            file_name="polarization_statistics.csv",
            mime="text/csv",
            use_container_width=True
        )

if __name__ == "__main__":
    main()
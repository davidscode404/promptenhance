import streamlit as st
import os
import fal_client
from dotenv import load_dotenv
import requests
from datetime import datetime
import glob

# Load environment variables
load_dotenv()

# Create generated_images directory if it doesn't exist
os.makedirs("./generated_images", exist_ok=True)

# Configure the page
st.set_page_config(page_title="Prompt Enhance", layout="wide")

# Improved CSS with uniform spacing and proportions
st.markdown("""
<style>
    /* Main container styling */
    .block-container {
        padding: 2rem 1rem;
        max-width: 100%;
    }
    
    /* Uniform spacing between all elements */
    .element-container {
        margin-bottom: 1rem !important;
    }
    
    /* Consistent text input styling */
    .stTextInput > div > div > input {
        height: 2.5rem !important;
        font-size: 14px !important;
        border-radius: 6px !important;
    }
    
    /* Consistent text area styling */
    .stTextArea > div > div > textarea {
        font-size: 14px !important;
        line-height: 1.4 !important;
        border-radius: 6px !important;
        resize: none !important;
    }
    
    /* Uniform button styling */
    .stButton > button {
        width: 100% !important;
        height: 2.5rem !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        border-radius: 6px !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4) !important;
        color: white !important;
    }
    
    /* Secondary button styling */
    .stButton > button:not([kind="primary"]) {
        background-color: #343a40 !important;
        color: #ffffff !important;
        border: 1px solid #495057 !important;
    }
    
    /* Button hover effects */
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Disabled button styling */
    .stButton > button:disabled {
        opacity: 0.5 !important;
        cursor: not-allowed !important;
        transform: none !important;
    }
    
    /* Column spacing */
    .css-1d391kg {
        gap: 1rem !important;
    }
    
    /* Section dividers */
    .section-divider {
        border-top: 2px solid #e9ecef;
        margin: 2rem 0 1.5rem 0;
        padding-top: 1.5rem;
    }
    
    /* Placeholder styling */
    .content-placeholder {
        width: 100%;
        aspect-ratio: 16/9;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        border: 2px dashed #495057;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: system-ui, -apple-system, sans-serif;
        font-size: 14px;
        font-weight: 500;
        color: #adb5bd;
        transition: all 0.3s ease;
    }
    
    .content-placeholder:hover {
        border-color: #6c757d;
        background: linear-gradient(135deg, #34495e 0%, #3d566e 100%);
    }
    
    /* Image styling */
    .stImage > img {
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        transition: transform 0.2s ease !important;
    }
    
    .stImage > img:hover {
        transform: scale(1.02) !important;
    }
    
    /* Video styling */
    video {
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Section labels */
    .section-label {
        font-size: 16px;
        font-weight: 600;
        color: #495057;
        margin-bottom: 0.5rem;
        text-align: center;
        padding: 0.5rem;
        background-color: #f8f9fa;
        border-radius: 6px;
        border-left: 4px solid #4ecdc4;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for outputs, clear flags, and images
if 'output1_text' not in st.session_state:
    st.session_state.output1_text = ""
if 'output2_text' not in st.session_state:
    st.session_state.output2_text = ""
if 'clear_input1' not in st.session_state:
    st.session_state.clear_input1 = False
if 'clear_input2' not in st.session_state:
    st.session_state.clear_input2 = False
if 'image1_url' not in st.session_state:
    st.session_state.image1_url = None
if 'image2_url' not in st.session_state:
    st.session_state.image2_url = None
if 'blank_output1_text' not in st.session_state:
    st.session_state.blank_output1_text = ""
if 'blank_clear_input1' not in st.session_state:
    st.session_state.blank_clear_input1 = False
if 'blank_image1_url' not in st.session_state:
    st.session_state.blank_image1_url = None
if 'video_url' not in st.session_state:
    st.session_state.video_url = None
if 'output1_generated' not in st.session_state:
    st.session_state.output1_generated = False
if 'output2_generated' not in st.session_state:
    st.session_state.output2_generated = False
if 'blank_output1_generated' not in st.session_state:
    st.session_state.blank_output1_generated = False

# Function to enhance prompt using fal-ai
def enhance_prompt(input_text):
    """Enhance prompt using fal-ai video-prompt-generator"""
    try:
        def on_queue_update(update):
            if isinstance(update, fal_client.InProgress):
                for log in update.logs:
                    print(log["message"])

        result = fal_client.subscribe(
            "fal-ai/video-prompt-generator",
            arguments={
                "input_concept": input_text
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )
        
        if isinstance(result, dict) and 'prompt' in result:
            return result['prompt']
        elif isinstance(result, dict) and 'output' in result:
            return result['output']
        else:
            return str(result)
            
    except Exception as e:
        return f"Error: {str(e)}"

# Function to save video from URL
def save_video_from_url(video_url, prompt_text):
    """Download and save video from URL with unique filename"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        clean_prompt = "".join(c for c in prompt_text[:50] if c.isalnum() or c in (' ', '-', '_')).strip()
        clean_prompt = clean_prompt.replace(' ', '_')
        filename = f"{timestamp}_video_{clean_prompt}.mp4"
        filepath = os.path.join("./generated_images", filename)
        
        response = requests.get(video_url)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        return filepath
    except Exception as e:
        st.error(f"Error saving video: {str(e)}")
        return None

def get_most_recent_image():
    """Get the most recent image from the generated_images folder"""
    try:
        image_files = glob.glob("./generated_images/*.jpg")
        if len(image_files) < 1:
            return None
        image_files.sort(key=os.path.getmtime, reverse=True)
        return image_files[0]
    except Exception as e:
        print(f"Error getting most recent image: {str(e)}")
        return None

def generate_video(prompt_text, image_path):
    """Generate video using fal-ai kling-video with image"""
    try:
        def on_queue_update(update):
            if isinstance(update, fal_client.InProgress):
                for log in update.logs:
                    print(log["message"])

        image_url = fal_client.upload_file(image_path)

        result = fal_client.subscribe(
            "fal-ai/kling-video/v2.1/master/image-to-video",
            arguments={
                "prompt": prompt_text,
                "image_url": image_url,
                "aspect_ratio": "16:9",
                
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )
        
        video_url = None
        if isinstance(result, dict) and 'video' in result:
            video_url = result['video']['url'] if isinstance(result['video'], dict) else result['video']
        elif isinstance(result, dict) and 'url' in result:
            video_url = result['url']
        
        if video_url:
            saved_path = save_video_from_url(video_url, prompt_text)
            if saved_path:
                st.success(f"Video saved as: {os.path.basename(saved_path)}")
            st.info(f"Used image: {os.path.basename(image_path)}")
            return video_url
        else:
            return None
            
    except Exception as e:
        st.error(f"Error generating video: {str(e)}")
        return None

def get_recent_images():
    """Get the two most recent images from the generated_images folder"""
    try:
        image_files = glob.glob("./generated_images/*.jpg")
        if len(image_files) < 2:
            return None, None
        image_files.sort(key=os.path.getmtime, reverse=True)
        return image_files[0], image_files[1]
    except Exception as e:
        print(f"Error getting recent images: {str(e)}")
        return None, None

def generate_multi_image(prompt_text):
    """Generate multi-image using fal-ai flux-pro with recent images"""
    try:
        image1_path, image2_path = get_recent_images()
        
        if not image1_path or not image2_path:
            st.error("Need at least 2 generated images to create multi-image")
            return None
        
        def on_queue_update(update):
            if isinstance(update, fal_client.InProgress):
                for log in update.logs:
                    print(log["message"])

        result = fal_client.subscribe(
            "fal-ai/flux-pro/kontext/max/multi",
            arguments={
                "prompt": prompt_text,
                "image_urls": [
                    fal_client.upload_file(image1_path), 
                    fal_client.upload_file(image2_path)
                ]
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )
        
        image_url = None
        if isinstance(result, dict) and 'images' in result and len(result['images']) > 0:
            image_url = result['images'][0]['url']
        elif isinstance(result, dict) and 'image' in result:
            image_url = result['image']['url'] if isinstance(result['image'], dict) else result['image']
        elif isinstance(result, dict) and 'url' in result:
            image_url = result['url']
        
        if image_url:
            saved_path = save_image_from_url(image_url, f"multi_{prompt_text}")
            if saved_path:
                st.success(f"Multi-image saved as: {os.path.basename(saved_path)}")
                st.info(f"Used images: {os.path.basename(image1_path)} + {os.path.basename(image2_path)}")
            return image_url
        else:
            return None
            
    except Exception as e:
        st.error(f"Error generating multi-image: {str(e)}")
        return None

def save_image_from_url(image_url, prompt_text):
    """Download and save image from URL with unique filename"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        clean_prompt = "".join(c for c in prompt_text[:50] if c.isalnum() or c in (' ', '-', '_')).strip()
        clean_prompt = clean_prompt.replace(' ', '_')
        filename = f"{timestamp}_{clean_prompt}.jpg"
        filepath = os.path.join("./generated_images", filename)
        
        response = requests.get(image_url)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        return filepath
    except Exception as e:
        st.error(f"Error saving image: {str(e)}")
        return None

def generate_image(prompt_text):
    """Generate image using fal-ai imagen4"""
    try:
        def on_queue_update(update):
            if isinstance(update, fal_client.InProgress):
                for log in update.logs:
                    print(log["message"])

        result = fal_client.subscribe(
            "fal-ai/imagen4/preview",
            arguments={
                "prompt": prompt_text,
                "aspect_ratio": "16:9"
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )
        
        image_url = None
        if isinstance(result, dict) and 'images' in result and len(result['images']) > 0:
            image_url = result['images'][0]['url']
        elif isinstance(result, dict) and 'image' in result:
            image_url = result['image']['url'] if isinstance(result['image'], dict) else result['image']
        elif isinstance(result, dict) and 'url' in result:
            image_url = result['url']
        
        if image_url:
            saved_path = save_image_from_url(image_url, prompt_text)
            if saved_path:
                st.success(f"Image saved as: {os.path.basename(saved_path)}")
            return image_url
        else:
            return None
            
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

def create_placeholder(label):
    """Create a uniform placeholder for images/videos"""
    return f"""
    <div class="content-placeholder">
        <span>{label}</span>
    </div>
    """

# Main title
st.markdown('<h1 class="main-title">Prompt Enhance</h1>', unsafe_allow_html=True)

# Create main columns with proper spacing
col1, col2 = st.columns([1, 1], gap="large")

# SECTION 1 - Image Generation 1
with col1:
    st.text("Step 01: Generate an image: ")

    # Input row with uniform proportions
    input_col, prompt_col, reset_col = st.columns([3, 1, 1])
    
    with input_col:
        input_value1 = "" if st.session_state.clear_input1 else st.session_state.get("input1", "")
        user_input1 = st.text_input("", value=input_value1, placeholder="Enter prompt here...", key="input1", label_visibility="collapsed")
        if st.session_state.clear_input1:
            st.session_state.clear_input1 = False
    
    with prompt_col:
        if st.button("Prompt", key="enhance_btn1", use_container_width=True):
            if user_input1.strip():
                with st.spinner("Enhancing prompt..."):
                    enhanced_prompt = enhance_prompt(user_input1)
                    st.session_state.output1_text = enhanced_prompt
                    st.session_state.output1_generated = True
                    st.rerun()
            else:
                st.warning("Please enter some text first!")
    
    with reset_col:
        if st.button("🔄", key="reset_btn1", use_container_width=True):
            st.session_state.output1_text = ""
            st.session_state.output1_generated = False
            st.session_state.clear_input1 = True
            st.session_state.image1_url = None
            st.rerun()
    
    # Content row with uniform proportions
    text_col, image_col = st.columns([3, 2])
    
    with text_col:
        if st.session_state.output1_generated:
            st.session_state.output1_text = st.text_area("", value=st.session_state.output1_text, key="output1", height=120)
        else:
            st.text_area("", value=st.session_state.output1_text, disabled=True, key="output1_readonly", height=120)
        
        generate_disabled = not st.session_state.output1_text.strip()
        if st.button("Generate Image 01", key="generate_btn1", disabled=generate_disabled, use_container_width=True):
            if st.session_state.output1_text.strip():
                with st.spinner("Generating image..."):
                    image_url = generate_image(st.session_state.output1_text)
                    if image_url:
                        st.session_state.image1_url = image_url
                        st.rerun()
                    else:
                        st.error("Failed to generate image")
    
    with image_col:
        if st.session_state.image1_url:
            st.image(st.session_state.image1_url, use_container_width=True)
        else:
            st.markdown(create_placeholder("🖼️"), unsafe_allow_html=True)

# SECTION 3 - Multi-Image Generation (moved to left column)
with col1:
    st.text("Step 03: Combine images:")

    # Input row
    input_col3, prompt_col3, reset_col3 = st.columns([3, 1, 1])
    
    with input_col3:
        input_value3 = "" if st.session_state.blank_clear_input1 else st.session_state.get("blank_input1", "")
        user_input3 = st.text_input("", value=input_value3, placeholder="Enter prompt here...", key="blank_input1", label_visibility="collapsed")
        if st.session_state.blank_clear_input1:
            st.session_state.blank_clear_input1 = False
    
    with prompt_col3:
        if st.button("Prompt", key="enhance_btn3", use_container_width=True):
            if user_input3.strip():
                with st.spinner("Enhancing prompt..."):
                    enhanced_prompt = enhance_prompt(user_input3)
                    st.session_state.blank_output1_text = enhanced_prompt
                    st.session_state.blank_output1_generated = True
                    st.rerun()
            else:
                st.warning("Please enter some text first!")
    
    with reset_col3:
        if st.button("🔄", key="reset_btn3", use_container_width=True):
            st.session_state.blank_output1_text = ""
            st.session_state.blank_output1_generated = False
            st.session_state.blank_clear_input1 = True
            st.session_state.blank_image1_url = None
            st.rerun()
    
    # Content row
    text_col3, image_col3 = st.columns([3, 2])
    
    with text_col3:
        if st.session_state.blank_output1_generated:
            st.session_state.blank_output1_text = st.text_area("", value=st.session_state.blank_output1_text, key="blank_output1", height=120)
        else:
            st.text_area("", value=st.session_state.blank_output1_text, disabled=True, key="blank_output1_readonly", height=120)
        
        # Multi-image generation button
        multi_disabled = not st.session_state.blank_output1_text.strip()
        if st.button("Generate Image 03", key="multi_btn", disabled=multi_disabled, use_container_width=True):
            if st.session_state.blank_output1_text.strip():
                with st.spinner("Generating multi-image..."):
                    multi_image_url = generate_multi_image(st.session_state.blank_output1_text)
                    if multi_image_url:
                        st.session_state.blank_image1_url = multi_image_url
                        st.rerun()
                    else:
                        st.error("Failed to generate multi-image")
    
    with image_col3:
        if st.session_state.blank_image1_url:
            st.image(st.session_state.blank_image1_url, use_container_width=True)
        else:
            st.markdown(create_placeholder("🖼️"), unsafe_allow_html=True)

# SECTION 2 - Image Generation 2 (right column)
with col2:
    st.text("Step 02: Generate another image:")

    # Input row
    input_col2, prompt_col2, reset_col2 = st.columns([3, 1, 1])
    
    with input_col2:
        input_value2 = "" if st.session_state.clear_input2 else st.session_state.get("input2", "")
        user_input2 = st.text_input("", value=input_value2, placeholder="Enter prompt here...", key="input2", label_visibility="collapsed")
        if st.session_state.clear_input2:
            st.session_state.clear_input2 = False
    
    with prompt_col2:
        if st.button("Prompt", key="enhance_btn2", use_container_width=True):
            if user_input2.strip():
                with st.spinner("Enhancing prompt..."):
                    enhanced_prompt = enhance_prompt(user_input2)
                    st.session_state.output2_text = enhanced_prompt
                    st.session_state.output2_generated = True
                    st.rerun()
            else:
                st.warning("Please enter some text first!")
    
    with reset_col2:
        if st.button("🔄", key="reset_btn2", use_container_width=True):
            st.session_state.output2_text = ""
            st.session_state.output2_generated = False
            st.session_state.clear_input2 = True
            st.session_state.image2_url = None
            st.rerun()
    
    # Content row
    text_col2, image_col2 = st.columns([3, 2])
    
    with text_col2:
        if st.session_state.output2_generated:
            st.session_state.output2_text = st.text_area("", value=st.session_state.output2_text, key="output2", height=120)
        else:
            st.text_area("", value=st.session_state.output2_text, disabled=True, key="output2_readonly", height=120)
        
        generate_disabled2 = not st.session_state.output2_text.strip()
        if st.button("Generate Image 02", key="generate_btn2", disabled=generate_disabled2, use_container_width=True):
            if st.session_state.output2_text.strip():
                with st.spinner("Generating image..."):
                    image_url = generate_image(st.session_state.output2_text)
                    if image_url:
                        st.session_state.image2_url = image_url
                        st.rerun()
                    else:
                        st.error("Failed to generate image")
    
    with image_col2:
        if st.session_state.image2_url:
            st.image(st.session_state.image2_url, use_container_width=True)
        else:
            st.markdown(create_placeholder("🖼️"), unsafe_allow_html=True)

# SECTION 4 - Video Generation (right column, below image generation 2)
with col2:
    st.text("Step 04: Generate video:")
    
    # Video display area (smaller)
    video_col1, video_col2, video_col3 = st.columns([1, 2, 1])
    with video_col2:
        if st.session_state.video_url:
            st.video(st.session_state.video_url, autoplay=True, loop=True)
        else:
            st.markdown(create_placeholder("🎬"), unsafe_allow_html=True)
    
    # Video generation button below the video
    video_disabled = not st.session_state.blank_output1_text.strip()
    if st.button("Generate Video", key="video_btn", disabled=video_disabled, use_container_width=True):
        if st.session_state.blank_output1_text.strip():
            recent_image = get_most_recent_image()
            if recent_image:
                with st.spinner("Generating video..."):
                    video_url = generate_video(st.session_state.blank_output1_text, recent_image)
                    if video_url:
                        st.session_state.video_url = video_url
                        st.rerun()
                    else:
                        st.error("Failed to generate video")
            else:
                st.error("No images found in generated_images folder")
import streamlit as st
from groq import Groq
import requests
from PIL import Image
from io import BytesIO

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# FAL API key (if available)
FAL_KEY = st.secrets.get("FAL_API_KEY", None)

# Page config
st.set_page_config(
    page_title="RoomGenie - AI Renovation Planner", 
    layout="wide", 
    page_icon="🧞‍♂️"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .tagline {
        text-align: center;
        color: #888;
        font-style: italic;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 0.8rem;
        border: none;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🧞‍♂️ RoomGenie</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Renovation Planning & Visualization</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">"Professional renovation plans with AI-generated visuals"</p>', unsafe_allow_html=True)

st.markdown("---")

# Simple input
user_input = st.text_area(
    "✨ Describe your dream renovation:",
    placeholder="e.g., Modern kitchen, ₹50,000 budget, white cabinets, marble countertops, brass fixtures",
    height=120,
    help="Include: room type, budget, colors, materials, style"
)

def generate_image_fal(prompt):
    """Generate image using FAL.ai - very reliable and fast"""
    try:
        if not FAL_KEY:
            return None
        
        import fal_client
        
        # Enhanced prompt for interior design
        enhanced_prompt = f"professional interior design photography, {prompt}, high quality, well lit, modern, clean, architectural photography, 8k"
        
        result = fal_client.subscribe(
            "fal-ai/flux/schnell",
            arguments={
                "prompt": enhanced_prompt[:512],
                "image_size": "landscape_16_9",
                "num_inference_steps": 4,
                "num_images": 1
            },
            with_logs=False,
            on_queue_update=lambda update: None,
        )
        
        # Get image URL
        if result and 'images' in result and len(result['images']) > 0:
            image_url = result['images'][0]['url']
            
            # Download image
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                return Image.open(BytesIO(response.content))
        
        return None
        
    except:
        return None

# Generate button
if st.button("🚀 Generate My Dream Room", type="primary"):
    
    if not user_input or not user_input.strip():
        st.warning("⚠️ Please describe your dream renovation!")
        st.stop()
    
    # Progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Two columns
    plan_col, image_col = st.columns([1.2, 1])
    
    # Generate plan
    with plan_col:
        status_text.text("🧞‍♂️ Creating renovation plan...")
        progress_bar.progress(20)
        
        try:
            system_prompt = """You are RoomGenie, an expert interior designer. Create detailed, practical renovation plans."""

            user_prompt = f"""{user_input}

Create a comprehensive renovation plan with:

## 1. Design Vision
- Style and theme
- **Color Palette** (specific colors)
- **Key Materials**
- Mood

## 2. Budget Breakdown
Itemized costs

## 3. Timeline
Week-by-week (4 weeks)

## 4. Visual Description
One detailed paragraph describing the finished room with specific colors, furniture, lighting, textures."""

            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=2500
            )
            
            plan = response.choices[0].message.content
            progress_bar.progress(50)
            
            st.success("✅ Renovation Plan Ready!")
            st.markdown(plan)
            
            # Extract visual description
            visual_desc = ""
            if "visual description" in plan.lower():
                lines = plan.split('\n')
                capture = False
                for line in lines:
                    if "visual description" in line.lower():
                        capture = True
                        continue
                    if capture and line.strip():
                        if line.strip().startswith('#'):
                            break
                        visual_desc += line.strip() + " "
                        if len(visual_desc) > 300:
                            break
            
            if len(visual_desc) < 50:
                visual_desc = user_input[:250]
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            progress_bar.empty()
            status_text.empty()
            st.stop()
    
    # Generate image
    with image_col:
        status_text.text("🎨 Generating visualization...")
        progress_bar.progress(70)
        
        if FAL_KEY:
            st.info("⏳ Generating high-quality image with FAL.ai (15-30 seconds)...")
            
            generated_image = generate_image_fal(visual_desc.strip())
            
            progress_bar.progress(100)
            status_text.empty()
            
            if generated_image:
                st.success("✅ Visualization Generated!")
                st.image(generated_image, caption="Your Dream Room", use_container_width=True)
                
                # Download
                buf = BytesIO()
                generated_image.save(buf, format="PNG")
                st.download_button(
                    label="📥 Download Image",
                    data=buf.getvalue(),
                    file_name="roomgenie.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ Image generation issue. Your plan is ready!")
        else:
            st.info("💡 Add FAL_API_KEY to Secrets for image generation")
            st.markdown("Get free API key at: https://fal.ai/")
    
    progress_bar.empty()

# Sidebar
with st.sidebar:
    st.markdown("### 🧞‍♂️ RoomGenie")
    st.markdown("""
    AI renovation planning + visualization
    
    **100% FREE**
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Setup")
    
    if FAL_KEY:
        st.success("✅ FAL.ai connected")
    else:
        st.warning("⚠️ No FAL API key")
        st.info("""
**To enable images:**
1. Go to fal.ai
2. Sign up (FREE)
3. Get API key
4. Add to Streamlit Secrets:
   `FAL_API_KEY = "key-xxx"`
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>Built by Kanav Chauhan</strong></p>
    <p><a href='https://github.com/KanavChauhan23' target='_blank'>GitHub</a></p>
</div>
""", unsafe_allow_html=True)

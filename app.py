import streamlit as st
from groq import Groq
import requests
from PIL import Image
from io import BytesIO
import time

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# FAL API key
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

def generate_image_fal_direct(prompt):
    """Generate image using FAL.ai REST API directly - more reliable"""
    try:
        if not FAL_KEY:
            return None, "No FAL API key found"
        
        # FAL.ai REST API endpoint for FLUX Schnell
        url = "https://fal.run/fal-ai/flux/schnell"
        
        headers = {
            "Authorization": f"Key {FAL_KEY}",
            "Content-Type": "application/json"
        }
        
        # Enhanced prompt for interior design
        enhanced_prompt = f"professional interior design photograph, {prompt}, high quality, well lit, modern, clean, architectural photography, photorealistic, 8k"
        
        payload = {
            "prompt": enhanced_prompt[:512],
            "image_size": "landscape_16_9",
            "num_inference_steps": 4,
            "num_images": 1,
            "enable_safety_checker": False
        }
        
        # Make request
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        # Check response
        if response.status_code == 200:
            result = response.json()
            
            # FAL returns image URL
            if 'images' in result and len(result['images']) > 0:
                image_url = result['images'][0]['url']
                
                # Download the image
                img_response = requests.get(image_url, timeout=30)
                if img_response.status_code == 200:
                    return Image.open(BytesIO(img_response.content)), None
                else:
                    return None, f"Failed to download image from URL: {img_response.status_code}"
            else:
                return None, f"No images in response: {result}"
        else:
            error_msg = f"FAL API returned {response.status_code}: {response.text[:200]}"
            return None, error_msg
        
    except Exception as e:
        return None, f"Exception: {str(e)}"

# Generate button
if st.button("🚀 Generate My Dream Room", type="primary"):
    
    if not user_input or not user_input.strip():
        st.warning("⚠️ Please describe your dream renovation!")
        st.stop()
    
    # Check FAL key
    if not FAL_KEY:
        st.error("❌ FAL_API_KEY not found in Streamlit Secrets!")
        st.info("""
**To add your FAL API key:**

1. Go to Settings → Secrets in Streamlit Cloud
2. Add this line:
   ```
   FAL_API_KEY = "your-key-here"
   ```
3. Save and restart the app
        """)
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
- **Color Palette** (specific colors with hex codes if possible)
- **Key Materials** (wood types, metals, fabrics)
- Mood and atmosphere

## 2. Budget Breakdown
Itemized costs that total the budget

## 3. Timeline
Week-by-week schedule (4 weeks)

## 4. Visual Description
Write ONE detailed paragraph (100-150 words) describing the finished room. Include:
- Exact colors of walls, furniture, accents
- All furniture pieces and their materials
- Lighting (natural and artificial)
- Layout and spatial feel
- Textures and finishes
- Overall atmosphere

Make it vivid and photorealistic!"""

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
            
            # Extract visual description for image
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
        status_text.text("🎨 Generating visualization with FAL.ai...")
        progress_bar.progress(60)
        
        st.info("⏳ Generating high-quality image... This takes 10-20 seconds. Please wait...")
        
        generated_image, error_msg = generate_image_fal_direct(visual_desc.strip())
        
        progress_bar.progress(100)
        status_text.empty()
        
        if generated_image:
            st.success("✅ Visualization Generated!")
            st.image(generated_image, caption="Your Dream Room (AI-Generated)", use_container_width=True)
            
            # Download button
            buf = BytesIO()
            generated_image.save(buf, format="PNG")
            st.download_button(
                label="📥 Download High-Quality Image",
                data=buf.getvalue(),
                file_name="roomgenie_visualization.png",
                mime="image/png",
                use_container_width=True
            )
        else:
            st.error(f"❌ Image generation failed!")
            
            if error_msg:
                st.error(f"**Error details:** {error_msg}")
            
            st.info("""
**Troubleshooting:**

1. **Check your FAL API key:**
   - Go to https://fal.ai/dashboard
   - Make sure your key is valid
   - Copy the FULL key

2. **In Streamlit Secrets, it should be:**
   ```
   FAL_API_KEY = "your-complete-key-here"
   ```
   (No extra spaces, include the full key)

3. **Verify FAL account:**
   - Make sure you're signed up at fal.ai
   - Check if you have any usage limits

Your renovation plan is ready above! Images will work once the API key is configured correctly.
            """)
    
    progress_bar.empty()
    
    st.markdown("---")
    st.info("💡 **Tip**: Screenshot or bookmark this page to save your plan!")

# Sidebar
with st.sidebar:
    st.markdown("### 🧞‍♂️ About RoomGenie")
    st.markdown("""
    AI-powered renovation planning with high-quality visualizations!
    
    **Features:**
    - 📋 Detailed design plans
    - 💰 Budget breakdowns
    - 📅 Timelines
    - 🎨 AI-generated images (FAL.ai)
    
    **100% FREE**
    """)
    
    st.markdown("---")
    
    # Show API key status
    if FAL_KEY:
        st.success("✅ FAL API Key: Connected")
        st.caption(f"Key starts with: {FAL_KEY[:10]}...")
    else:
        st.error("❌ FAL API Key: Not Found")
        st.info("""
**Setup FAL.ai:**

1. Go to https://fal.ai
2. Sign up (FREE)
3. Go to Dashboard → API Keys
4. Copy your key
5. Add to Streamlit Secrets:
   `FAL_API_KEY = "key..."`
        """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Tips for Best Results")
    st.markdown("""
    **Include in your description:**
    - Room type
    - Budget (₹)
    - Specific colors
    - Materials (wood, marble, etc.)
    - Style (modern, rustic, etc.)
    - Lighting preferences
    
    **More details = better plan & image!**
    """)
    
    st.markdown("---")
    
    st.markdown("### 📝 Example")
    
    st.code("""
"Modern bedroom, ₹35,000 budget.
Soft white walls (#F8F8F8), warm
oak bed frame, sage green accents,
natural lighting, cozy textiles,
minimalist design"
    """, language=None)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Technology")
    st.markdown("""
    **Planning AI**: Groq (Llama 3.3 70B)  
    **Image AI**: FAL.ai (FLUX Schnell)  
    
    🟢 **Status**: Active
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>✨ Built with ❤️ by Kanav Chauhan ✨</strong></p>
    <p>
        <a href='https://github.com/KanavChauhan23' target='_blank'>GitHub</a> | 
        <a href='https://github.com/KanavChauhan23/ai-home-renovation-agent' target='_blank'>Source Code</a>
    </p>
    <p style='font-size: 12px; margin-top: 10px;'>
        🧞‍♂️ RoomGenie - AI Renovation Planning & Visualization
    </p>
</div>
""", unsafe_allow_html=True)

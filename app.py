import streamlit as st
from groq import Groq
import requests
from PIL import Image
from io import BytesIO
import time

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Check for Hugging Face API token (optional, falls back to Pollinations)
HF_TOKEN = st.secrets.get("HUGGINGFACE_API_KEY", None)

st.set_page_config(page_title="AI Home Renovation Planner", layout="wide", page_icon="🏠")

st.title("🏠 AI Home Renovation Planner")
st.markdown("**Plan your renovation smartly using AI** - Get detailed plans + AI-generated visualization!")

# Room type selection
room_type = st.selectbox(
    "Select room type",
    ["Kitchen", "Bedroom", "Bathroom", "Living Room", "Dining Room", "Home Office", "Study Room"]
)

# Budget input
budget = st.number_input(
    "Enter budget (USD)",
    min_value=1000,
    max_value=1000000,
    value=5000,
    step=500
)

def generate_image_pollinations(prompt):
    """Generate image using Pollinations.ai (no API key needed)"""
    try:
        # Clean and encode prompt
        clean_prompt = prompt.replace('\n', ' ').strip()
        # Pollinations API endpoint
        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(clean_prompt)}?width=1024&height=768&nologo=true"
        
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        return None
    except Exception as e:
        st.warning(f"Pollinations API error: {str(e)}")
        return None

def generate_image_huggingface(prompt):
    """Generate image using Hugging Face Stable Diffusion"""
    try:
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        # Clean prompt
        clean_prompt = prompt.replace('\n', ' ').strip()[:500]  # Limit length
        
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": clean_prompt},
            timeout=60
        )
        
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        elif response.status_code == 503:
            st.info("⏳ Model is loading... trying alternative method...")
            time.sleep(3)
            return None
        else:
            return None
    except Exception as e:
        st.warning(f"Hugging Face API error: {str(e)}")
        return None

# Generate button
if st.button("🚀 Generate Renovation Plan", use_container_width=True):
    if budget < 1000:
        st.warning("⚠️ Please enter a budget of at least $1000")
        st.stop()
    
    # Step 1: Generate renovation plan
    with st.spinner("🤖 Creating your detailed renovation plan..."):
        try:
            detailed_prompt = f"""Create a comprehensive renovation plan for a {room_type} with a budget of ${budget}.

Please provide:

1. **Design Vision**:
   - Overall design concept and style (modern, rustic, minimalist, etc.)
   - Color palette (primary, secondary, accent colors - be specific with color names)
   - Key materials and textures
   - Atmosphere and mood

2. **Detailed Budget Breakdown**:
   - Paint & Supplies: $X
   - Flooring: $X
   - Lighting: $X
   - Furniture: $X (list main pieces)
   - Fixtures & Hardware: $X
   - Decor & Accessories: $X
   - Labor/Installation: $X
   - Contingency (10%): $X
   - TOTAL: ${budget}

3. **4-Week Timeline**:
   - Week 1: Planning & preparation
   - Week 2: Core updates (paint, flooring)
   - Week 3: Installation (furniture, fixtures)
   - Week 4: Finishing touches

4. **AI Visualization Prompt** (IMPORTANT - Be very descriptive):
   Write a detailed prompt for AI image generation that describes the FINAL renovated {room_type}. Include:
   - Exact view/angle (e.g., "wide shot from doorway")
   - Specific colors used
   - All furniture and their materials
   - Lighting type and ambiance
   - Textures and materials visible
   - Overall atmosphere
   - Style keywords (modern, cozy, bright, etc.)
   
Example format: "A bright modern kitchen with white subway tile backsplash, light oak floating shelves, marble countertops, brass fixtures, pendant lights over island, large window with natural light, potted herbs on windowsill, professional interior photography, magazine quality, 8k"

Format with clear headers."""

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert interior designer. Provide detailed renovation plans with specific costs and comprehensive visual descriptions suitable for AI image generation."
                    },
                    {
                        "role": "user",
                        "content": detailed_prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=3000
            )
            
            renovation_plan = chat_completion.choices[0].message.content
            
            # Display the plan
            st.success("✅ Renovation Plan Generated!")
            st.markdown("---")
            st.markdown(renovation_plan)
            
        except Exception as e:
            st.error(f"❌ Error generating plan: {str(e)}")
            st.stop()
    
    # Step 2: Extract image prompt and generate visualization
    st.markdown("---")
    with st.spinner("🎨 Generating AI visualization of your renovated space..."):
        try:
            # Extract the AI visualization prompt from the plan
            # Look for the section after "AI Visualization Prompt" or "AI Image Generation Prompt"
            if "AI Visualization Prompt" in renovation_plan or "AI Image Generation Prompt" in renovation_plan:
                # Try to extract the prompt
                lines = renovation_plan.split('\n')
                image_prompt = ""
                capture = False
                
                for line in lines:
                    if "AI Visualization Prompt" in line or "AI Image Generation Prompt" in line or "visualization prompt" in line.lower():
                        capture = True
                        continue
                    if capture:
                        if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('**'):
                            image_prompt += line.strip() + " "
                        if len(image_prompt) > 100:  # Got enough
                            break
                
                # Enhance the prompt for better images
                enhanced_prompt = f"Professional interior design photograph, {image_prompt.strip()}, high quality, 8k, architectural digest style, bright natural lighting, wide angle"
                
                st.info(f"🎨 **Image Prompt**: {enhanced_prompt[:200]}...")
                
                # Try to generate image
                generated_image = None
                
                # Try Hugging Face first if token available
                if HF_TOKEN:
                    st.info("⏳ Generating with Hugging Face Stable Diffusion (15-30 seconds)...")
                    generated_image = generate_image_huggingface(enhanced_prompt)
                
                # Fallback to Pollinations if HF failed or no token
                if not generated_image:
                    st.info("⏳ Generating with Pollinations.ai...")
                    generated_image = generate_image_pollinations(enhanced_prompt)
                
                if generated_image:
                    st.success("✅ AI Visualization Generated!")
                    st.image(generated_image, caption=f"AI-Generated Visualization of Your Renovated {room_type}", use_container_width=True)
                    
                    # Provide download button
                    buf = BytesIO()
                    generated_image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    st.download_button(
                        label="📥 Download Visualization",
                        data=byte_im,
                        file_name=f"{room_type.lower()}_renovation_${budget}.png",
                        mime="image/png"
                    )
                else:
                    st.warning("⚠️ Could not generate image. The renovation plan is still available above!")
                    
            else:
                st.info("💡 Image generation prompt not clearly identified in the plan. Using general prompt...")
                general_prompt = f"Professional interior design photo of a beautifully renovated {room_type}, modern style, budget ${budget}, high quality, architectural photography"
                generated_image = generate_image_pollinations(general_prompt)
                if generated_image:
                    st.image(generated_image, caption=f"AI Visualization - {room_type}", use_container_width=True)
                
        except Exception as e:
            st.warning(f"⚠️ Could not generate visualization: {str(e)}")
            st.info("Your renovation plan is still available above!")
    
    st.markdown("---")
    st.info("💡 **Tip**: Save this plan and the visualization! Consult with a professional contractor before starting work.")

# Sidebar
with st.sidebar:
    st.markdown("### 📖 How It Works")
    st.markdown("""
    1. **Select** your room type
    2. **Enter** your budget
    3. **Click** Generate
    4. Get:
       - 📋 Detailed renovation plan
       - 💰 Budget breakdown
       - 📅 Timeline
       - 🎨 **AI-generated visualization!**
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Budget Guidelines")
    st.markdown("""
    - **Refresh**: $2,000 - $5,000
    - **Update**: $5,000 - $15,000
    - **Full Reno**: $15,000+
    """)
    
    st.markdown("---")
    
    st.markdown("### 🎨 Image Generation")
    api_status = "🟢 Pollinations.ai (Free)"
    if HF_TOKEN:
        api_status = "🟢 Hugging Face SD (Premium)"
    st.markdown(f"**Status**: {api_status}")
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Powered By")
    st.markdown("""
    - **Planning**: Groq AI (Llama 3.3)
    - **Images**: Stable Diffusion
    - ✅ 100% FREE
    - ✅ Unlimited use
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with ❤️ by Kanav Chauhan | 
    <a href='https://github.com/KanavChauhan23' target='_blank'>GitHub</a> | 
    <a href='https://github.com/KanavChauhan23/ai-home-renovation-agent' target='_blank'>Source Code</a>
    </p>
</div>
""", unsafe_allow_html=True)

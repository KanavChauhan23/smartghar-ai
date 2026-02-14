import streamlit as st
from groq import Groq
import requests
from PIL import Image
from io import BytesIO
import time

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
HF_TOKEN = st.secrets["HUGGINGFACE_API_KEY"]

# Page config
st.set_page_config(
    page_title="AI Home Renovation Planner", 
    layout="wide", 
    page_icon="🏠"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
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
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.75rem;
        border: none;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏠 AI Home Renovation Planner</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Get professional renovation plans with AI-generated visualizations</p>', unsafe_allow_html=True)

st.markdown("---")

# Simple text input for user question
user_input = st.text_area(
    "💬 Describe your renovation project:",
    placeholder="e.g., I want to renovate my kitchen with a budget of $5,000. I prefer a modern look with white cabinets.",
    height=100,
    help="Be specific! Include room type, budget, style preferences, and any special requirements."
)

def generate_image_huggingface(prompt):
    """Generate image using a reliable Hugging Face model"""
    try:
        # Using Stable Diffusion v1.5 (more reliable than XL)
        API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        # Create professional prompt
        enhanced_prompt = f"professional interior design photography, {prompt}, high quality, architectural photography, well lit, 4k, professional staging"
        
        payload = {
            "inputs": enhanced_prompt[:500],
            "parameters": {
                "negative_prompt": "blurry, distorted, ugly, low quality, amateur, messy, cluttered",
                "num_inference_steps": 25,
            }
        }
        
        # First attempt
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 503:
            # Model loading - wait and retry
            st.info("⏳ Model is loading... Please wait 20 seconds...")
            time.sleep(20)
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            st.error(f"Image API returned status {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"Image generation error: {str(e)}")
        return None

# Generate button
if st.button("🚀 Generate Renovation Plan", type="primary"):
    
    if not user_input or not user_input.strip():
        st.warning("⚠️ Please describe your renovation project first!")
        st.stop()
    
    # Create two columns for results
    plan_col, image_col = st.columns([1.2, 1])
    
    # STEP 1: Generate renovation plan
    with plan_col:
        with st.spinner("🤖 Creating your renovation plan..."):
            try:
                # Enhanced prompt for better responses
                system_prompt = """You are an expert interior designer and renovation consultant. 
                
When given a renovation request:
1. Analyze the budget and room type
2. Provide a DETAILED renovation plan with specific items and costs
3. Include a complete budget breakdown
4. Provide a realistic timeline
5. At the END, write a detailed visual description for AI image generation

Format your response professionally with clear sections."""

                user_prompt = f"""{user_input}

Please provide:

1. **Project Overview**: Brief summary of the renovation

2. **Design Concept**: 
   - Style and theme
   - Color palette (specific colors)
   - Key materials and finishes

3. **Budget Breakdown**: 
   List specific items with costs that add up to the total budget

4. **Timeline**: 
   Realistic week-by-week schedule

5. **Visual Description** (for AI image generation):
   Describe in detail how the finished room will look - include colors, furniture, lighting, textures, layout. Make it vivid and specific enough for an AI to generate a realistic image."""

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=2500
                )
                
                renovation_plan = chat_completion.choices[0].message.content
                
                # Display plan
                st.success("✅ Renovation Plan Ready!")
                st.markdown(renovation_plan)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.stop()
    
    # STEP 2: Generate image
    with image_col:
        with st.spinner("🎨 Generating visualization..."):
            try:
                # Extract visual description from plan
                visual_prompt = ""
                if "Visual Description" in renovation_plan or "visual description" in renovation_plan.lower():
                    lines = renovation_plan.split('\n')
                    capture = False
                    for line in lines:
                        if "visual description" in line.lower():
                            capture = True
                            continue
                        if capture and line.strip():
                            if line.strip().startswith('#'):
                                break
                            visual_prompt += line.strip() + " "
                            if len(visual_prompt) > 300:
                                break
                
                # If no visual description found, extract room details from user input
                if len(visual_prompt) < 50:
                    visual_prompt = f"beautiful renovated interior space based on: {user_input[:200]}"
                
                # Generate image
                generated_image = generate_image_huggingface(visual_prompt.strip())
                
                if generated_image:
                    st.success("✅ Visualization Generated!")
                    st.image(
                        generated_image, 
                        caption="AI-Generated Visualization",
                        use_container_width=True
                    )
                    
                    # Download button
                    buf = BytesIO()
                    generated_image.save(buf, format="PNG")
                    st.download_button(
                        label="📥 Download Image",
                        data=buf.getvalue(),
                        file_name="renovation_visualization.png",
                        mime="image/png",
                        use_container_width=True
                    )
                else:
                    st.warning("⚠️ Image generation unavailable. Your plan is ready in the left column!")
                    
            except Exception as e:
                st.warning(f"Image generation issue: {str(e)}")

# Sidebar
with st.sidebar:
    st.markdown("### 📖 How to Use")
    st.markdown("""
    **1.** Describe your renovation
    - Mention room type
    - State your budget  
    - Add style preferences
    
    **2.** Click Generate
    
    **3.** Receive:
    - 📋 Detailed plan
    - 💰 Budget breakdown
    - 📅 Timeline
    - 🎨 AI visualization
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Example Prompts")
    st.code("""
"Renovate my small bedroom 
with $3,000. I want a 
minimalist, calming design 
with light colors."
    """)
    
    st.code("""
"Kitchen makeover for $8,000. 
Modern farmhouse style with 
white cabinets and wood 
accents."
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Technology")
    st.markdown("""
    **AI Planning**  
    Groq (Llama 3.3)
    
    **Image Generation**  
    Stable Diffusion v1.5
    
    **Status**: 🟢 Active
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>Built with ❤️ by Kanav Chauhan</strong></p>
    <p>
        <a href='https://github.com/KanavChauhan23' target='_blank'>GitHub</a> | 
        <a href='https://github.com/KanavChauhan23/ai-home-renovation-agent' target='_blank'>Source Code</a>
    </p>
</div>
""", unsafe_allow_html=True)

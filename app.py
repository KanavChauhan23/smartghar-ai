import streamlit as st
from groq import Groq

# ==============================
# Initialize Groq Client
# ==============================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="RoomGenie - AI Renovation Planner",
    layout="wide",
    page_icon="🧞‍♂️"
)

# ==============================
# Custom CSS
# ==============================
st.markdown("""
<style>
.main-header {
    font-size: 3.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}

.sub-header {
    text-align: center;
    color: #666;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    font-size: 1.1rem;
    font-weight: 600;
    padding: 0.8rem;
    border-radius: 10px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# Header
# ==============================
st.markdown('<h1 class="main-header">🧞‍♂️ RoomGenie</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Renovation Planning</p>', unsafe_allow_html=True)

st.markdown("---")

# ==============================
# User Input
# ==============================
user_input = st.text_area(
    "✨ Describe your renovation project:",
    placeholder="""
Example:
Modern bedroom, ₹40,000 budget,
white walls, wooden furniture,
minimalist style, good lighting
""",
    height=130,
    help="Include: Room type, Budget, Colors, Style, Materials"
)

# ==============================
# Example Prompts
# ==============================
with st.expander("📌 See Example Prompts"):
    st.code("""
Modern kitchen, ₹50,000 budget,
white cabinets, marble countertop,
brass handles, pendant lights
    """)
    
    st.code("""
Living room, ₹45,000,
warm colors, wooden sofa,
plants, cozy lighting
    """)

# ==============================
# Generate Button
# ==============================
if st.button("🚀 Generate Renovation Plan", type="primary"):

    if not user_input.strip():
        st.warning("⚠️ Please enter your renovation details.")
        st.stop()

    with st.spinner("🧞‍♂️ Creating your professional plan..."):
        try:

            # ==============================
            # System Prompt
            # ==============================
            system_prompt = """
You are RoomGenie, a professional interior designer
with 20 years of experience.

You create:
- Practical renovation plans
- Realistic budgets
- Clear timelines
- Useful shopping lists
- Detailed AI image prompts

Your advice is realistic and budget-friendly.
"""

            # ==============================
            # User Prompt
            # ==============================
            user_prompt = f"""
User Request:
{user_input}

Create a complete renovation plan with:

# 1. Project Overview
- Summary
- Budget
- Timeline

# 2. Design Vision
- Style
- Color palette (with names)
- Materials
- Mood

# 3. Budget Breakdown
Provide item-wise costing:
- Paint
- Flooring
- Lighting
- Furniture
- Decor
- Labor
- Contingency (10%)
- TOTAL

# 4. 4-Week Timeline
Week-by-week tasks

# 5. Shopping List
- Must-Have
- Nice-to-Have
- Future Upgrades

# 6. Pro Tips
- Saving money
- Maintenance
- Best practices

# 7. AI Image Prompt (TEXT ONLY)
Write ONE detailed prompt for AI image generation.
Include:
- Camera angle
- Colors
- Furniture
- Lighting
- Textures
- Atmosphere
- Style keywords

Make it realistic and photorealistic.
"""

            # ==============================
            # Call Groq API
            # ==============================
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=3500
            )

            result = response.choices[0].message.content

            # ==============================
            # Display Output
            # ==============================
            st.success("✅ Renovation Plan Ready!")
            st.markdown("---")
            st.markdown(result)

            st.markdown("---")
            st.info("💡 Tip: Use the AI Image Prompt in tools like Midjourney, DALL·E, Leonardo, etc.")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


# ==============================
# Sidebar
# ==============================
with st.sidebar:

    st.markdown("## 🧞‍♂️ About RoomGenie")

    st.markdown("""
RoomGenie helps you create:

✅ Professional Renovation Plans  
✅ Budget Breakdown  
✅ Timeline  
✅ Shopping List  
✅ AI Image Prompt (Text)

**100% Free**
    """)

    st.markdown("---")

    st.markdown("## 💡 Best Tips")

    st.markdown("""
✔ Mention room type  
✔ Give exact budget  
✔ Tell color preference  
✔ Mention style  
✔ Add special needs
    """)

    st.markdown("---")

    st.markdown("### 🚀 Built By Kanav")


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
        🧞‍♂️ RoomGenie - Professional Renovation Planning with AI Visualization
    </p>
</div>
""", unsafe_allow_html=True)

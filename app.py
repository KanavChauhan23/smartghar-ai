import streamlit as st
from groq import Groq

# ===============================
# Initialize AI Client
# ===============================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="SmartGhar AI - Renovation Planner",
    layout="wide",
    page_icon="🏠"
)

# ===============================
# Custom CSS (Professional UI)
# ===============================
st.markdown("""
<style>

body {
    background-color: #fafafa;
}

.main-title {
    font-size: 3rem;
    font-weight: 800;
    color: #4F46E5;
    text-align: center;
}

.sub-title {
    text-align: center;
    font-size: 1.1rem;
    color: #555;
    margin-bottom: 20px;
}

.input-box textarea {
    border-radius: 12px !important;
    font-size: 16px !important;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(135deg,#4F46E5,#7C3AED);
    color: white;
    font-size: 18px;
    font-weight: 600;
    padding: 12px;
    border-radius: 12px;
    border: none;
}

.stButton>button:hover {
    transform: scale(1.02);
    background: linear-gradient(135deg,#7C3AED,#4F46E5);
}

.section-box {
    background: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0px 0px 12px rgba(0,0,0,0.05);
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# ===============================
# Header
# ===============================
st.markdown('<h1 class="main-title">🏠 SmartGhar AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Smart Renovation Planning for Indian Homes</p>', unsafe_allow_html=True)

st.markdown("---")

# ===============================
# Sidebar (Left Panel)
# ===============================
with st.sidebar:

    st.markdown("## 🇮🇳 About SmartGhar AI")

    st.markdown("""
✅ Easy Renovation Plans  
✅ Budget in Rupees  
✅ Timeline  
✅ Material List  
✅ Contractor-Friendly  
✅ AI Image Prompt  
✅ Work Estimation  
✅ Cost Saving Tips  

**100% Free for India**
    """)

    st.markdown("---")

    st.markdown("## 🛠️ For Whom?")

    st.markdown("""
✔ Home Owners  
✔ Local Contractors  
✔ Interior Workers  
✔ Builders  
✔ Small Businesses  
    """)

    st.markdown("---")

    st.markdown("## 💡 How To Use")

    st.markdown("""
1️⃣ Write your requirement  
2️⃣ Click Generate  
3️⃣ Share plan with worker  
4️⃣ Start work  
    """)

    st.markdown("---")

    st.markdown("## 🚀 Extra Features")

    st.markdown("""
📄 Download Plan  
📱 Mobile Friendly  
🧮 Cost Calculator  
🧱 Material Guide  
🔧 Work Checklist  
    """)

    st.markdown("---")

    st.markdown("### ❤️ Built By Kanav")

# ===============================
# Input Section
# ===============================
st.markdown("## ✍️ Describe Your Renovation")

st.markdown("""
Write in simple words. Example format:

**Room Type + Budget + Needs**
""")

user_input = st.text_area(
    "",
    placeholder="""
Example:

Kitchen renovation, ₹20,000 budget
Need cabinets, gas stove, sink
White color, easy cleaning
Small size kitchen
    """,
    height=160,
    key="input",
    help="Write room type, budget, and needs clearly"
)

# ===============================
# Easy Examples
# ===============================
with st.expander("📌 Click to See Easy Examples"):

    st.code("""
Bedroom, ₹30,000 budget
Double bed, cupboard, lights
Light blue walls
Simple design
    """)

    st.code("""
Bathroom, ₹25,000
Tiles, wash basin, shower
Anti-slip floor
Good drainage
    """)

    st.code("""
Living room, ₹40,000
Sofa, TV unit, ceiling lights
Warm colors
Space for guests
    """)

    st.code("""
Small kitchen, ₹20,000
Gas stove, sink, shelves
White tiles
Low maintenance
    """)


# ===============================
# Generate Button
# ===============================
if st.button("🚀 Generate Smart Plan"):

    if not user_input.strip():
        st.warning("⚠️ Please write your renovation details.")
        st.stop()

    with st.spinner("🤖 SmartGhar AI is preparing your plan..."):

        try:

            # ===============================
            # System Prompt
            # ===============================
            system_prompt = """
You are SmartGhar AI.

You are an expert Indian home renovation consultant.

Your job:
- Use simple English
- Easy for workers to understand
- Clear costing in INR
- Practical materials
- Local market based advice
- Step by step explanation

Write in simple words.
Avoid complex technical language.
"""

            # ===============================
            # User Prompt
            # ===============================
            user_prompt = f"""
User Requirement:
{user_input}

Create a renovation plan with:

## 1. Project Overview (Very Simple)
- Room Name
- Budget
- Work Needed
- Area Size (Approx)
- Main Goal

## 2. Design & Look
- Style
- Wall Colors
- Floor Type
- Lighting
- Furniture

## 3. Budget Details (In Rupees)
Give realistic costing:
- Paint
- Tiles/Floor
- Furniture
- Electrical
- Plumbing
- Labour
- Material
- Extra (10%)

## 4. Work Timeline (4 Weeks)
Week-wise work plan

## 5. Material List
Write clear shopping list

## 6. Worker Instructions
Simple steps for mason, electrician, plumber

## 7. Money Saving Tips
How to reduce cost

## 8. AI Image Prompt
Write ONE detailed prompt for image generation

Use very simple language.
Make it suitable for Indian workers.
"""

            # ===============================
            # Call AI
            # ===============================
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.6,
                max_tokens=3500
            )

            result = response.choices[0].message.content

            # ===============================
            # Display Output
            # ===============================
            st.success("✅ Your Smart Renovation Plan is Ready!")

            st.markdown("---")

            st.markdown(result)

            st.markdown("---")

            st.info("📌 Tip: Share this plan with your contractor on WhatsApp.")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ===============================
# Footer
# ===============================
st.markdown("---")

st.markdown("""
<center>
SmartGhar AI 🇮🇳 | Made for Indian Homes | Powered by AI  
</center>
""", unsafe_allow_html=True)


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
        🏠 SmartGhar AI - Renovation PlanneRoom
    </p>
</div>
""", unsafe_allow_html=True)

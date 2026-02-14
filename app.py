import streamlit as st
from openai import OpenAI
import time

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI Home Renovation", layout="wide", page_icon="🏠")

st.title("🏠 AI Home Renovation Planner")
st.markdown("Plan your renovation smartly using AI (FREE version)")

st.markdown("""
### 💡 Try These Examples:
- Kitchen renovation ideas under $5,000
- Modern bedroom makeover with minimalist design
- Small bathroom upgrade suggestions
""")

st.markdown("---")

user_input = st.text_input(
    "Enter your renovation question:",
    placeholder="e.g., I want to renovate my kitchen with a $3000 budget"
)

if st.button("🚀 Generate Renovation Plan", use_container_width=True):
    if not user_input.strip():
        st.warning("⚠️ Please enter a question first.")
        st.stop()
    
    with st.spinner("🤖 AI is planning your renovation..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Changed to free tier model
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful home renovation expert. Provide practical, budget-conscious renovation advice."
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                max_tokens=300,  # Reduced to save quota
                temperature=0.7
            )
            
            st.success("✅ Renovation Plan Generated!")
            st.markdown("### 📋 Your Renovation Plan")
            st.write(response.choices[0].message.content)
            st.markdown("---")
            st.info("💡 **Tip:** Wait 30 seconds before making another request to avoid rate limits.")
            
        except Exception as e:
            error_message = str(e)
            
            if "429" in error_message or "rate_limit" in error_message.lower():
                st.error("⏱️ **Rate Limit Reached!**")
                st.warning("OpenAI free tier allows only 3 requests per minute. Please wait 60 seconds and try again.")
                st.info("💡 **Tip:** If you need more requests, consider using Groq API (completely free, 14,400/day)")
            elif "quota" in error_message.lower():
                st.error("❌ **Quota Issue**")
                st.warning("Your free trial quota may have been used. Check: https://platform.openai.com/usage")
            else:
                st.error(f"❌ Error: {error_message}")

with st.sidebar:
    st.markdown("### ⚠️ Usage Limits")
    st.markdown("""
    **OpenAI Free Tier:**
    - 3 requests per minute
    - 200 requests per day
    - Wait between requests!
    """)
    
    st.markdown("---")
    
    st.markdown("### 📖 How to Use")
    st.markdown("""
    1. Enter your question
    2. Click Generate
    3. **Wait 30 seconds** before next request
    """)

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with ❤️ by Kanav Chauhan | 
    <a href='https://github.com/KanavChauhan23' target='_blank'>GitHub</a>
    </p>
</div>
""", unsafe_allow_html=True)

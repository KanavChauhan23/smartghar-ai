# 🏡 SmartGhar AI

<div align="center">

![SmartGhar AI Banner](https://img.shields.io/badge/SmartGhar-AI%20Powered-blueviolet?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39+-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**AI-Powered Home Renovation Planning for Indian Homes**

[Live Demo](https://smartghar-ai.streamlit.app/) • [Report Bug](https://github.com/KanavChauhan23/smartghar-ai/issues) • [Request Feature](https://github.com/KanavChauhan23/smartghar-ai/issues)

*आपके सपनों का घर, AI की मदद से | Your Dream Home, Powered by AI*

</div>

---

## 🌟 Overview

**SmartGhar AI** is an intelligent home renovation planning platform specifically designed for Indian homes and budgets. Powered by advanced AI, it generates comprehensive renovation plans with realistic pricing, timelines, and AI-generated visualization prompts — all in seconds.

### Why SmartGhar AI?

- 🇮🇳 **Built for India** - Realistic pricing in ₹, local brand recommendations, climate-appropriate suggestions
- 💰 **Budget-Conscious** - Detailed cost breakdowns with actual Indian market prices
- 🎨 **AI Visualization** - Generates prompts for free image generation via Google Gemini
- ⚡ **Lightning Fast** - Complete renovation plans in 20-30 seconds
- 📚 **Comprehensive** - Design vision, shopping guides, timelines, and pro tips
- 🆓 **100% Free** - No hidden costs, no API limits, unlimited use

---

## ✨ Features

### 📋 Comprehensive Planning
- **Project Overview** with budget allocation and timeline estimates
- **Design Vision** with style themes, color palettes (with hex codes), and material specifications
- **Detailed Budget Breakdown** itemized for paint, flooring, furniture, fixtures, labor, and contingency
- **Week-by-Week Timeline** for organized implementation

### 🛒 Smart Shopping
- **Indian Brand Recommendations** (Asian Paints, Pepperfry, IKEA India, Fabindia, etc.)
- **Local Store Suggestions** for best value purchases
- **Money-Saving Tips** for budget optimization
- **Where to Buy Guide** categorized by budget levels

### 💪 DIY Guidance
- **DIY vs Professional breakdown** - What you can do yourself vs. when to hire experts
- **Safety recommendations** for electrical and structural work
- **Step-by-step guidance** for paint, furniture assembly, and decor

### 🎨 AI Visualization
- **Detailed AI Image Prompts** generated based on your specific design
- **Direct Integration** with Google Gemini and ImageFX
- **Easy Copy** functionality for prompt transfer
- **Free Image Generation** - No API costs or limits

### 🏠 Indian Market Focus
- Pricing in **Indian Rupees (₹)**
- **Climate-appropriate** material and design suggestions
- **Cultural sensitivity** in design recommendations
- **Local vendor** and marketplace guidance

---

## 🚀 Live Demo

**Try it now:** [https://smartghar-ai.streamlit.app/](https://smartghar-ai.streamlit.app/)

### Sample Input
```
Bedroom renovation, ₹35,000 budget. Modern minimalist design with soft white 
walls, warm oak bed frame, sage green accents, natural lighting, and cozy 
cotton textiles.
```

---

## 📸 Screenshots

### Home Interface
![Home Interface](screenshots/home.png)
*Clean, intuitive interface for entering renovation requirements*

### Renovation Plan Output
![Plan Output](screenshots/plan-output.png)
*Comprehensive renovation plan with budget breakdown and timeline*

### AI Prompt Generation
![AI Prompt](screenshots/ai-prompt.png)
*Generated AI visualization prompts with easy copy functionality*

> **Note:** Add actual screenshots to a `/screenshots` folder in your repo

---

## 🛠️ Tech Stack

### Core Technologies
- **Frontend Framework:** [Streamlit](https://streamlit.io/) - Fast, beautiful web apps in Python
- **AI Model:** [Groq](https://groq.com/) (Llama 3.3 70B) - Lightning-fast AI inference
- **Language:** Python 3.9+
- **Image Generation:** Google Gemini / ImageFX integration

### Key Libraries
- `streamlit` - Web application framework
- `groq` - AI inference API client
- `urllib.parse` - URL encoding for Gemini integration

---

## 💻 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Groq API key ([Get free key](https://console.groq.com/))

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/KanavChauhan23/smartghar-ai.git
   cd smartghar-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.streamlit/secrets.toml` file:
   ```toml
   GROQ_API_KEY = "your-groq-api-key-here"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   ```
   Navigate to http://localhost:8501
   ```

---

## 📁 Project Structure

```
smartghar-ai/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
│
├── .streamlit/
│   └── secrets.toml      # API keys (local only, not in Git)
│
└── screenshots/          # App screenshots for README
    ├── home.png
    ├── plan-output.png
    └── ai-prompt.png
```

---

## 🎯 Use Cases

### For Homeowners
- Planning renovations with realistic budgets
- Getting professional design advice
- Understanding cost breakdowns before hiring contractors
- Visualizing design concepts

### For Interior Design Students
- Learning budget planning and material selection
- Understanding professional renovation workflows
- Exploring design styles and color combinations

### For Real Estate Professionals
- Quick renovation cost estimates
- Helping clients visualize potential improvements
- Budget planning for property flips

### For DIY Enthusiasts
- Understanding which tasks can be DIY vs. professional
- Getting step-by-step guidance
- Learning about materials and tools

---

## 🔑 Key Differentiators

| Feature | SmartGhar AI | Traditional Planning |
|---------|-------------|---------------------|
| **Speed** | 30 seconds | Days to weeks |
| **Cost** | Free | ₹5,000 - ₹50,000+ |
| **AI Visualization** | Integrated prompts | Hire designer |
| **Indian Market** | ✅ Focused | ❌ Generic |
| **Budget Accuracy** | Local pricing | Often inflated |
| **DIY Guidance** | ✅ Included | Rarely provided |

---

## 🌍 Indian Market Features

### Pricing
- All costs in **₹ (INR)**
- Based on actual Indian market rates
- Includes GST considerations where relevant
- City-tier appropriate recommendations

### Brand Recommendations
- **Paint:** Asian Paints, Berger, Dulux
- **Furniture:** Pepperfry, Urban Ladder, IKEA India, Fabindia
- **Tiles:** Kajaria, Somany
- **Hardware:** Hafele, D-Decor
- **Decor:** HomeStop, Home Centre, Zara Home

### Climate Considerations
- Ventilation for Indian climate
- Moisture-resistant materials for humid regions
- Heat-reflective options for hot climates

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Ideas for Contributions
- Add more Indian city-specific pricing
- Support for multiple languages (Hindi, Tamil, etc.)
- Integration with additional AI image generators
- Material cost calculator
- Contractor recommendation system
- Before/After photo gallery

---

## 📝 Roadmap

- [x] Core renovation planning functionality
- [x] AI image prompt generation
- [x] Indian market pricing
- [x] Google Gemini integration
- [ ] Multi-language support (Hindi, Tamil, Telugu)
- [ ] Material cost calculator
- [ ] Contractor marketplace integration
- [ ] User accounts for saving plans
- [ ] Mobile app version
- [ ] AR visualization support

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Kanav Chauhan**

- GitHub: [@KanavChauhan23](https://github.com/KanavChauhan23)
- LinkedIn: [Kanav Chauhan](https://linkedin.com/in/kanavchauhan23)
- Portfolio: [Your Portfolio URL](https://kanav-public.netlify.app/)

---

## 🙏 Acknowledgments

- **Groq** for providing fast, powerful AI inference
- **Streamlit** for the amazing web framework
- **Google Gemini** for free AI image generation
- The open-source community for inspiration and tools

---

## 📊 Stats

![GitHub Stars](https://img.shields.io/github/stars/KanavChauhan23/smartghar-ai?style=social)
![GitHub Forks](https://img.shields.io/github/forks/KanavChauhan23/smartghar-ai?style=social)
![GitHub Issues](https://img.shields.io/github/issues/KanavChauhan23/smartghar-ai)

---

<div align="center">

**Made with ❤️ in India**

If you found this project helpful, please consider giving it a ⭐!

[⬆ Back to Top](#-smartghar-ai)

</div>

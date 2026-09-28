# 👑 AURA — Women's Empowerment, Style & Mindset Sanctuary

**AURA** is an all-in-one personal growth, styling, grooming, and emotional wellness sanctuary designed to empower women to step into their sovereignty, cultivate fierce independence, curate their signature elegance, and nurture deep self-love.

Now with full support for **Streamlit Cloud Deployment**, **GitHub Upload**, and **Live AI Key Integration** (Google Gemini & Groq)!

---

## 🌟 The Core Pillars of AURA

1. **🛡️ Mental Strength & Independence**:
   - *The Boundary Vault*: Non-apologetic scripts for Career, Family Pressure, Dating Standards, and Friendships.
   - *Cognitive Reframer (CBT Engine)*: Transforms self-doubt, body anxiety, or imposter syndrome into sovereign, grounded truth.
   - *The Charisma & Poise Blueprint*: Voice pause, soft eye contact, and executive communication.
2. **👗 Wardrobe Architecture & Styling**:
   - *Silhouette Formula*: Body shape analysis (Hourglass, Pear, Rectangle, Round/Apple, Inverted Triangle) with power formulas.
   - *The 15-Piece French-Chic Capsule*: 15 timeless, high-mileage essentials creating 50+ combinations.
   - *Occasion Lookbooks*: Career, French-Chic, Romantic Evening, and Quiet Luxury.
3. **✨ Looks, Skincare & Physical Poise**:
   - *Thin-to-Thick Skincare Protocol*: The master layering order (Cleanser → Toner → Actives → Ceramides → SPF 50+).
   - *The Posture & Walking Protocol*: Crown alignment line and scent-stacking rituals.
4. **💖 Maia: AI Emotional Companion & Therapist**:
   - Empathetic CBT coaching with Google Gemini, Groq, or built-in offline wisdom engine.
   - 4-7-8 Nervous System Reset breathing meditation tool.
5. **📖 Daily Self-Love Rituals & Habits**:
   - Daily Power Affirmations and Queen Habits Tracker.
   - Private Self-Love Journal with export download.

---

## 🚀 How to Run Locally

### Option A: Run via Streamlit (Recommended)
Make sure you are in the project folder and run:
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
Your browser will open automatically at `http://localhost:8501`.

### Option B: Run Standalone Web App
```bash
python run.py
```
Or simply double-click `index.html`.

---

## 🔑 AI API Key Configuration

Maia supports two high-performance AI engines (as well as a built-in offline wisdom engine that requires no key at all):

| Provider | Model | Free Tier Link |
| :--- | :--- | :--- |
| **Google Gemini** *(Recommended)* | `gemini-1.5-flash` | [Get Free Gemini API Key](https://aistudio.google.com/app/apikey) |
| **Groq** | `llama-3.3-70b-versatile` | [Get Free Groq API Key](https://console.groq.com/keys) |

### How to use your API key:
1. **Directly in the App**: In the Streamlit sidebar, select your provider and paste your key into the password field.
2. **Via Local Secrets**: Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and paste your key:
   ```toml
   GEMINI_API_KEY = "AIzaSy..."
   ```

---

## 📦 How to Upload to GitHub

### Method 1: Upload via GitHub Web (No Git installation needed!)
1. Go to [github.com](https://github.com) and log in.
2. Click the **"+"** button at the top right and select **"New repository"**.
3. Name your repository (e.g. `aura-empowerher`), set it to **Public** or **Private**, and click **"Create repository"**.
4. On the next screen, click the link that says **"uploading an existing file"**.
5. Drag and drop the files from your folder:
   - `streamlit_app.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore`
   - `.streamlit/` folder (`config.toml` and `secrets.toml.example`)
   - `index.html`, `style.css`, `app.js`
6. Click **"Commit changes"**. Your project is now on GitHub!

### Method 2: Upload via Git Command Line
```bash
git init
git add .
git commit -m "Initial commit of AURA empowerment app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/aura-empowerher.git
git push -u origin main
```

---

## ☁️ How to Deploy to Streamlit Community Cloud (Free Hosting)

Once your code is on GitHub, you can publish it live to the web for free:

1. Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
2. Click **"New app"**.
3. Select your repository: `YOUR_USERNAME/aura-empowerher`.
4. Set Main file path to: `streamlit_app.py`.
5. Click **"Advanced settings"** -> **Secrets** tab, and paste your API key:
   ```toml
   GEMINI_API_KEY = "your-actual-gemini-key"
   ```
6. Click **"Deploy"**!

Your app will be live with a public URL (e.g. `https://aura-empowerher.streamlit.app`) that you and others can access anywhere on mobile or desktop!

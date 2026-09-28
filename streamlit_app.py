import streamlit as st
import os
import json
import requests
from datetime import datetime

# ==============================================================================
# 1. PAGE CONFIGURATION & LUXURY STYLING
# ==============================================================================

st.set_page_config(
    page_title="AURA | Women's Empowerment, Style & Mindset",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Luxury Rose-Gold / Silk Aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    h1, h2, h3, .serif-font {
        font-family: 'Playfair Display', serif !important;
    }
    
    /* Hero Banner Card */
    .hero-card {
        background: linear-gradient(135deg, #5B2333 0%, #936F78 50%, #C77D87 100%);
        color: #ffffff;
        padding: 2.2rem;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(91, 35, 51, 0.2);
        margin-bottom: 1.5rem;
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #FFFFFF;
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        font-style: italic;
        color: #FDF6F4;
        line-height: 1.6;
    }
    
    /* Aesthetic Content Cards */
    .aura-card {
        background-color: #FFFFFF;
        border: 1px solid rgba(232, 165, 152, 0.35);
        border-radius: 16px;
        padding: 1.4rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .aura-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(199, 125, 135, 0.12);
    }
    
    .badge-pill {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        background-color: #F9EBEA;
        color: #5B2333;
        margin-bottom: 0.5rem;
    }
    
    .script-box {
        background: #FDF6F4;
        border-left: 4px solid #C77D87;
        padding: 1rem;
        border-radius: 8px;
        font-style: italic;
        color: #5B2333;
        margin: 0.6rem 0;
        font-weight: 500;
    }
    
    /* Button refinement */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #936F78 0%, #5B2333 100%);
        color: white;
        border: none;
        border-radius: 9999px;
        padding: 0.5rem 1.4rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    div.stButton > button:first-child:hover {
        opacity: 0.92;
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CONSTANTS & DOMAIN KNOWLEDGE
# ==============================================================================

AFFIRMATIONS = [
  "I do not chase; I attract. My worth is non-negotiable, and I am building an independent life I truly adore.",
  "I honor my boundaries without apologizing. Saying 'No' to others is saying 'Yes' to my peace.",
  "My beauty is in my poise, my intellect, and the kindness I show to myself first.",
  "I am not in competition with any woman; I celebrate sisterhood while fiercely running my own race.",
  "I release the urge to be liked by everyone. Respecting myself is infinitely more important.",
  "My financial independence is my sacred freedom. I make wise decisions for my present and my future.",
  "I am worthy of romantic love that brings peace, emotional safety, and effortless reciprocity.",
  "I hold space for my emotions without letting them define my power. I am resilient and calm.",
  "My body is a temple of vitality and grace. I dress it with pride and treat it with devotion.",
  "I am whole on my own. Anyone who enters my life is a bonus, not my missing half."
]

MAIA_SYSTEM_PROMPT = """You are Maia, an empathetic, wise, and empowering emotional wellness mentor and life coach specialized in women's personal empowerment, self-worth, emotional regulation, and quiet strength.

Your core guidelines:
1. Tone: Deeply validating, compassionate, grounded, articulate, and sovereign. Never dismissive or patronizing.
2. Cognitive Reframing: Use gentle Cognitive Behavioral Therapy (CBT) principles to identify cognitive distortions (e.g., people-pleasing, imposter syndrome, catastrophic thinking, self-criticism) and reframe them into empowered, evidence-based truths.
3. Assertiveness & Standards: Encourage self-respect, financial autonomy, high standards in relationships, and setting boundaries without apologizing.
4. Actionable Steps: Close your responses with 1 gentle, immediate step the user can take today to honor herself.
5. Safety: You are a supportive mentor, not a clinical doctor. If someone expresses severe self-harm or medical emergency, urge them with deep warmth to reach out to professional emergency resources (e.g. 988 lifeline). Keep responses concise, warm, and structured with clear spacing.
"""

# ==============================================================================
# 3. SIDEBAR NAVIGATION & API CONFIGURATION
# ==============================================================================

with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h2 style="font-family: 'Playfair Display', serif; color: #5B2333; margin-bottom: 0;">AURA</h2>
            <p style="font-size: 0.8rem; letter-spacing: 2px; text-transform: uppercase; color: #936F78; font-weight: 600;">Sanctuary</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu = st.radio(
        "Explore Sanctuary",
        [
            "🌸 Sanctuary Home",
            "🛡️ Mental Strength & Independence",
            "👗 Wardrobe Architecture & Styling",
            "✨ Looks, Skincare & Poise",
            "💖 Maia: AI Therapist & Guide",
            "📖 Daily Habits & Journal"
        ]
    )
    
    st.markdown("---")
    
    # AI API Configuration
    st.markdown("### 🔑 AI Companion Engine")
    
    api_provider = st.selectbox(
        "AI Provider",
        ["Google Gemini", "Groq", "Built-in Compassionate AI (Free)"]
    )
    
    # Detect stored secret or let user input
    stored_gemini_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
    stored_groq_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
    
    user_api_key = ""
    if api_provider == "Google Gemini":
        user_api_key = st.text_input(
            "Gemini API Key",
            value=stored_gemini_key,
            type="password",
            help="Get your free Gemini API key at https://aistudio.google.com/app/apikey"
        )
        if not user_api_key:
            st.caption("👉 [Get Free Gemini API Key](https://aistudio.google.com/app/apikey)")
            st.info("No key entered? Maia will seamlessly use her built-in wisdom engine.")
    elif api_provider == "Groq":
        user_api_key = st.text_input(
            "Groq API Key",
            value=stored_groq_key,
            type="password",
            help="Get your fast, free API key at https://console.groq.com/keys"
        )
        if not user_api_key:
            st.caption("👉 [Get Free Groq API Key](https://console.groq.com/keys)")
            st.info("No key entered? Maia will seamlessly use her built-in wisdom engine.")
    else:
        st.success("Using built-in offline wisdom engine. No key needed!")

    st.markdown("---")
    st.caption("✨ Built with love for sovereign, independent women.")

# ==============================================================================
# 4. AI GENERATION HELPER
# ==============================================================================

def query_ai_therapist(user_prompt: str, chat_history_list: list) -> str:
    """Dispatches user prompt to Google Gemini, Groq, or the built-in empathetic engine."""
    
    # 1. Try Google Gemini API if selected and key provided
    if api_provider == "Google Gemini" and user_api_key.strip():
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={user_api_key.strip()}"
            
            # Format message history
            contents = []
            for msg in chat_history_list[-6:]:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg["content"]}]})
            contents.append({"role": "user", "parts": [{"text": user_prompt}]})
            
            payload = {
                "contents": contents,
                "systemInstruction": {"parts": [{"text": MAIA_SYSTEM_PROMPT}]},
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 800}
            }
            
            resp = requests.post(url, json=payload, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                st.warning(f"Gemini API note: HTTP {resp.status_code}. Using built-in empathetic response.")
        except Exception as e:
            st.warning(f"Could not connect to Gemini API ({str(e)}). Switching to built-in response.")

    # 2. Try Groq API if selected and key provided
    if api_provider == "Groq" and user_api_key.strip():
        try:
            from groq import Groq
            client = Groq(api_key=user_api_key.strip())
            messages = [{"role": "system", "content": MAIA_SYSTEM_PROMPT}]
            for msg in chat_history_list[-6:]:
                messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": user_prompt})
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
            return completion.choices[0].message.content
        except Exception as e:
            st.warning(f"Could not connect to Groq API ({str(e)}). Switching to built-in response.")

    # 3. Built-in Offline Empathetic Engine Fallback
    prompt_lower = user_prompt.lower()
    if any(w in prompt_lower for w in ["overwhelm", "burnout", "tired", "exhausted", "too much"]):
        return (
            "Take a deep, slow breath and drop your shoulders away from your ears right now. 🌸\n\n"
            "You are carrying far too much on your shoulders, and you've been conditioned to believe that your worth is tied to how much you can endure. It isn't.\n\n"
            "**Here is your sovereign prescription for today:**\n"
            "1. Give yourself permission to do only the bare essentials today.\n"
            "2. Say a polite 'no' to anything optional.\n"
            "3. Step away from your screens for 20 minutes with a warm cup of tea.\n\n"
            "*You do not have to hold up the world. Rest is a sovereign right, not a luxury.*"
        )
    elif any(w in prompt_lower for w in ["people pleas", "say no", "boundary", "guilt"]):
        return (
            "I hear you so clearly, Queen. People-pleasing is often an old armor we wore to stay safe and accepted. "
            "But every time you say 'yes' to someone else when your spirit screams 'no', you betray yourself.\n\n"
            "**Remember this sacred truth:**\n"
            "• Boundaries are not walls to keep others out; they are doors that teach others how to love you properly.\n"
            "• You do not need to justify or over-explain. A calm, warm: *'I won't be able to commit to that, but thank you for thinking of me'* is a complete sentence.\n\n"
            "Take a moment and say that aloud right now. Feel how grounded it sounds."
        )
    elif any(w in prompt_lower for w in ["imposter", "smart", "career", "work", "fail", "belong"]):
        return (
            "Let me remind you of something non-negotiable: **You did not arrive here by accident.** "
            "Luck did not do the studying, the perseverance, or the late nights. You did.\n\n"
            "When imposter syndrome whispers: *'You don't belong here,'* your higher self answers: *'I belong in every room I step into, and I bring a fresh, valuable perspective.'*\n\n"
            "In your next meeting: Keep your posture tall, rest your hands open on the table, and speak at a calm, measured pace. You are ready."
        )
    elif any(w in prompt_lower for w in ["breakup", "heartbreak", "dating", "boyfriend", "ex", "love"]):
        return (
            "Your heart is so tender and brave for loving deeply. But listen closely: **Never shrink yourself or accept breadcrumbs just to avoid being alone.**\n\n"
            "A woman who knows her worth does not beg for consistency, respect, or intentionality. If someone is confusing you, that confusion is your answer. Step back into your magnetic center. "
            "Nourish your goals, your friendships, and your radiance. The right love will feel like peace, not a puzzle to decode."
        )
    elif any(w in prompt_lower for w in ["ugly", "body", "look", "weight", "skin", "pretty"]):
        return (
            "Look into your own eyes in the mirror for 10 seconds without critique. Look at the soul looking back at you.\n\n"
            "True beauty is not about matching an algorithm's airbrushed standard. True beauty is in your poise, the softness in your smile, the sparkle in your eyes when you speak about what you love, and the elegance with which you hold your posture.\n\n"
            "Nourish your skin with hydration and SPF, dress your unique body with high honor, and walk with the quiet grace of someone who knows she is irreplaceable."
        )
    else:
        return (
            "Thank you for sharing that with me. It takes real vulnerability to voice what we hold inside.\n\n"
            "Whatever you are navigating right now, remember that you do not have to have everything figured out this minute. Clarity comes from taking one intentional, grounded step at a time.\n\n"
            "**One gentle question for you:** What is one small, loving action you can do in the next 15 minutes that honors your well-being?"
        )

# ==============================================================================
# 5. TAB 1: SANCTUARY HOME
# ==============================================================================

if menu == "🌸 Sanctuary Home":
    # Hero Card
    if "affirmation_idx" not in st.session_state:
        st.session_state.affirmation_idx = 0
        
    current_aff = AFFIRMATIONS[st.session_state.affirmation_idx]
    
    st.markdown(f"""
        <div class="hero-card">
            <span class="badge-pill" style="background: rgba(255,255,255,0.25); color: #FFFFFF;">Today's Empowerment Anchor</span>
            <div class="hero-title">"{current_aff}"</div>
            <div class="hero-subtitle">— Daily Power Truth for the Sovereign Woman</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("✨ New Affirmation"):
            st.session_state.affirmation_idx = (st.session_state.affirmation_idx + 1) % len(AFFIRMATIONS)
            st.rerun()
            
    # Mood Check-In
    st.markdown("### 👑 Heart & Energy Check-in")
    st.write("How is your heart feeling today? Select an energy state for Maia's personalized guidance:")
    
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    selected_mood = None
    
    with m_col1:
        if st.button("👑 Radiant & Capable"): selected_mood = "radiant"
    with m_col2:
        if st.button("🌊 Overwhelmed"): selected_mood = "overwhelmed"
    with m_col3:
        if st.button("🕊️ Anxious / Doubtful"): selected_mood = "anxious"
    with m_col4:
        if st.button("🕯️ Seeking Grounding"): selected_mood = "grounding"
    with m_col5:
        if st.button("⚡ Ready to Conquer"): selected_mood = "conquer"
        
    if selected_mood == "radiant":
        st.success("**Maia's Note:** Carry this electric, centered feeling into every room you step into. When a woman knows her worth and holds high standards with warmth, she becomes an inspiration to everyone around her.")
    elif selected_mood == "overwhelmed":
        st.warning("**Maia's Note:** You do not have to solve everything today. Take a slow breath. Give yourself permission to pause, cancel non-urgent obligations, and do one tiny loving task at a time.")
    elif selected_mood == "anxious":
        st.info("**Maia's Note:** Anxiety is simply your body trying to protect you. Place one hand on your heart and one on your belly. Remind yourself: *'I am safe right now. I have survived 100% of my hard days.'*")
    elif selected_mood == "grounding":
        st.info("**Maia's Note:** Light your favorite candle, put on soft music, brew a warm tea, and remember that your own company is a sanctuary.")
    elif selected_mood == "conquer":
        st.success("**Maia's Note:** Direct this fire with laser clarity! Channel it into your creative vision, an independent financial milestone, or elevating your life standards.")

    st.markdown("---")
    
    # Core Growth Pillars
    st.markdown("### 🏛️ Your Four Pillars of Elevation")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown("""
        <div class="aura-card">
            <h4>🛡️ Mental Strength</h4>
            <p style="font-size: 0.85rem; color: #666;">Assertiveness scripts, imposter syndrome reframes, and boundary setting.</p>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="aura-card">
            <h4>👗 Wardrobe & Style</h4>
            <p style="font-size: 0.85rem; color: #666;">Body silhouette formulas, 15-piece capsule matrix, and power outfits.</p>
        </div>
        """, unsafe_allow_html=True)
    with p3:
        st.markdown("""
        <div class="aura-card">
            <h4>✨ Radiance & Poise</h4>
            <p style="font-size: 0.85rem; color: #666;">Thin-to-thick skincare rituals, posture alignment, and scent stacking.</p>
        </div>
        """, unsafe_allow_html=True)
    with p4:
        st.markdown("""
        <div class="aura-card">
            <h4>💖 Maia AI Mentor</h4>
            <p style="font-size: 0.85rem; color: #666;">Empathetic CBT coaching, emotional regulation, and unconditional validation.</p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 6. TAB 2: MENTAL STRENGTH & INDEPENDENCE
# ==============================================================================

elif menu == "🛡️ Mental Strength & Independence":
    st.markdown("## 🛡️ Mental Strength & Independence Academy")
    st.write("Cultivating unbreakable self-worth, unapologetic boundaries, and quiet inner steel.")
    
    tab_boundary, tab_reframe, tab_poise = st.tabs([
        "🛡️ The Boundary Vault", 
        "🧠 Cognitive Reframer (CBT)", 
        "👑 Charisma & Poise Blueprint"
    ])
    
    with tab_boundary:
        st.markdown("### The Boundary Vault: What To Say With Grace")
        category = st.selectbox(
            "Select Scenario Domain:",
            ["Work & Career", "Family Pressure", "Dating & Relationships", "Friendships & Energy"]
        )
        
        if category == "Work & Career":
            st.markdown("""
            <div class="aura-card">
                <span class="badge-pill">Scenario: Working Overtime / Weekends</span>
                <p style="font-size: 0.9rem; color: #555;">When asked to take on urgent work during personal time:</p>
                <div class="script-box">“I’m fully committed to delivering excellence on this, but my schedule is committed this evening. I will prioritize this first thing tomorrow at 9 AM.”</div>
                <p style="font-size: 0.8rem; color: #888;"><strong>Psychological Key:</strong> Never say 'I'm sorry.' An apology makes an innocent boundary sound like an error.</p>
            </div>
            
            <div class="aura-card">
                <span class="badge-pill">Scenario: Interrupted in Meetings</span>
                <p style="font-size: 0.9rem; color: #555;">When someone talks over you while presenting:</p>
                <div class="script-box">“Hold that thought, [Name]—I’d like to finish this point, and then I’m eager to hear your thoughts.”</div>
                <p style="font-size: 0.8rem; color: #888;"><strong>Psychological Key:</strong> Warm smile, steady tone, and direct eye contact without flinching.</p>
            </div>
            """, unsafe_allow_html=True)
            
        elif category == "Family Pressure":
            st.markdown("""
            <div class="aura-card">
                <span class="badge-pill">Scenario: Marriage / Dating Timeline Inquiries</span>
                <p style="font-size: 0.9rem; color: #555;">When relatives pry into your relationship status:</p>
                <div class="script-box">“I value my life and partnership too deeply to rush into anything that isn't extraordinary. When there is news worth sharing, you will be the first to know.”</div>
                <p style="font-size: 0.8rem; color: #888;"><strong>Psychological Key:</strong> Smile serenely and immediately redirect: 'How has your garden been doing?'</p>
            </div>
            
            <div class="aura-card">
                <span class="badge-pill">Scenario: Comments on Body or Plate</span>
                <p style="font-size: 0.9rem; color: #555;">When someone comments on what you are eating or your weight:</p>
                <div class="script-box">“I am feeling wonderful in my body and trusting my appetite, thank you. Let's focus on enjoying today's celebration.”</div>
            </div>
            """, unsafe_allow_html=True)
            
        elif category == "Dating & Relationships":
            st.markdown("""
            <div class="aura-card">
                <span class="badge-pill">Scenario: Last-Minute Low-Effort Invitations</span>
                <p style="font-size: 0.9rem; color: #555;">Late-night 'hang out' text with zero planning:</p>
                <div class="script-box">“I appreciate the thought, but I don’t do last-minute plans. Let’s plan something a few days in advance if you'd like to get together.”</div>
                <p style="font-size: 0.8rem; color: #888;"><strong>Psychological Key:</strong> High-value women do not sit waiting on someone's impulse.</p>
            </div>
            
            <div class="aura-card">
                <span class="badge-pill">Scenario: Inconsistent Communication</span>
                <p style="font-size: 0.9rem; color: #555;">Disappearing for days and casually reappearing:</p>
                <div class="script-box">“I really value consistent, intentional communication. It seems our rhythms are different, and I wish you all the best.”</div>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.markdown("""
            <div class="aura-card">
                <span class="badge-pill">Scenario: Emotional Trauma-Dumping</span>
                <p style="font-size: 0.9rem; color: #555;">When a friend unloads endless stress without asking how you are:</p>
                <div class="script-box">“I love you and care about you, but I don’t have the emotional capacity to hold this space today. Can we reconnect over the weekend?”</div>
                <p style="font-size: 0.8rem; color: #888;"><strong>Psychological Key:</strong> You are a friend, not an unpaid 24/7 therapist.</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_reframe:
        st.markdown("### 🧠 Cognitive Reframer (Turning Self-Doubt into Truth)")
        st.write("Write down a self-critical or fearful thought you've been having:")
        
        user_thought = st.text_area(
            "Self-Critical Thought:",
            placeholder="e.g. 'Everyone in the room is smarter than me and I don't belong here...'"
        )
        
        if st.button("✨ Reframe to Sovereign Truth"):
            if user_thought.strip():
                with st.spinner("Reframing with cognitive wisdom..."):
                    reframe_prompt = f"Please reframe this self-critical thought into an empowering, grounded, and sovereign truth based on CBT cognitive restructuring: '{user_thought}'"
                    reframe_ans = query_ai_therapist(reframe_prompt, [])
                    st.markdown(f"""
                        <div class="aura-card" style="border-left: 4px solid #5B2333; background: #FDF6F4;">
                            <span class="badge-pill">Higher-Self Truth</span>
                            <div style="font-size: 1rem; color: #5B2333; font-weight: 500; line-height: 1.6;">
                                {reframe_ans}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Please type a thought to reframe.")

    with tab_poise:
        st.markdown("### 👑 The Charisma & Poise Blueprint")
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.markdown("""
            <div class="aura-card">
                <h4>1. The Power of The Pause</h4>
                <p style="font-size: 0.85rem; color: #555;">Never rush to answer. When asked a tough question, pause for 2 full seconds. Stillness and measured speech communicate high authority and emotional regulation.</p>
            </div>
            """, unsafe_allow_html=True)
        with col_c2:
            st.markdown("""
            <div class="aura-card">
                <h4>2. The Soft Gaze</h4>
                <p style="font-size: 0.85rem; color: #555;">Maintain gentle eye contact on the bridge of the nose. When breaking eye contact, break to the side—never look down at the floor, which signals subordination.</p>
            </div>
            """, unsafe_allow_html=True)
        with col_c3:
            st.markdown("""
            <div class="aura-card">
                <h4>3. Drop the Apologies</h4>
                <p style="font-size: 0.85rem; color: #555;">Replace "Sorry to bother you" with "Thank you for your time." Replace "Does that make sense?" with "I look forward to your thoughts."</p>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# 7. TAB 3: WARDROBE ARCHITECTURE & STYLING
# ==============================================================================

elif menu == "👗 Wardrobe Architecture & Styling":
    st.markdown("## 👗 Wardrobe Architecture & Styling Elevation")
    st.write("Dressing with intention, honoring your silhouette, and building a magnetic, timeless wardrobe.")
    
    tab_sil, tab_cap, tab_look = st.tabs([
        "📐 Silhouette Formula", 
        "🧥 15-Piece French-Chic Capsule", 
        "✨ Curated Occasion Lookbooks"
    ])
    
    with tab_sil:
        st.markdown("### Find Your Natural Body Architecture")
        body_type = st.selectbox(
            "Select Your Body Silhouette:",
            ["Hourglass", "Pear / Triangle", "Rectangle / Athletic", "Round / Apple", "Inverted Triangle"]
        )
        
        if body_type == "Hourglass":
            st.markdown("""
            <div class="aura-card">
                <span class="badge-pill">Hourglass: Balanced bust & hips with defined waist</span>
                <p><strong>✨ Best Flattering Cuts:</strong> Wrap dresses, belted trenches, high-waisted tailored trousers, V-neck, and bias-cut midi skirts.</p>
                <p><strong>⚠️ Avoid:</strong> Shapeless boxy sack tunics that conceal your natural waistline.</p>
                <div class="script-box"><strong>Power Formula:</strong> Belted silk wrap midi dress + pointed-toe slingback heels + structured leather tote.</div>
            </div>
            """, unsafe_allow_html=True)
        elif body_type == "Pear / Triangle":
            st.markdown("""
            <div class="aura-card">
                <span class="badge-pill">Pear: Hips wider than shoulders</span>
                <p><strong>✨ Best Flattering Cuts:</strong> Boatnecks, structured shoulder blazers, A-line midi skirts that glide over hips, and statement necklaces.</p>
                <p><strong>⚠️ Avoid:</strong> Heavy cargo pockets on hips and low-rise skinny jeans.</p>
                <div class="script-box"><strong>Power Formula:</strong> Tailored blazer with subtle shoulder pads + crisp ivory blouse + wide-leg navy trousers.</div>
            </div>
            """, unsafe_allow_html=True)
        elif body_type == "Rectangle / Athletic":
            st.markdown("""
            <div class="aura-card">
                <span class="badge-pill">Rectangle: Lean, aligned proportions</span>
                <p><strong>✨ Best Flattering Cuts:</strong> Belts cinched over oversized blazers, fit-and-flare dresses, pleated trousers creating curves, and cowl necks.</p>
                <p><strong>⚠️ Avoid:</strong> Rigidly straight sack silhouettes with zero waist definition.</p>
                <div class="script-box"><strong>Power Formula:</strong> Oversized blazer cinched with a leather belt + tapered high-rise trousers + pointed pumps.</div>
            </div>
            """, unsafe_allow_html=True)
        elif body_type == "Round / Apple":
            st.markdown("""
            <div class="aura-card">
                <span class="badge-pill">Round / Apple: Fuller bust & midriff with shapely legs</span>
                <p><strong>✨ Best Flattering Cuts:</strong> Empire waists, deep V-necks that elongate the décolletage, fluid open duster coats, and monochromatic column dressing.</p>
                <p><strong>⚠️ Avoid:</strong> Tight horizontal waist belts directly across the tummy.</p>
                <div class="script-box"><strong>Power Formula:</strong> Monochrome black silk camisole + fluid duster coat + ankle-length slim trousers.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="aura-card">
                <span class="badge-pill">Inverted Triangle: Broad shoulders/bust with slender hips</span>
                <p><strong>✨ Best Flattering Cuts:</strong> Deep V-necks to break up shoulder width, wide-leg or pleated palazzo trousers to add volume to lower half, and peplum jackets.</p>
                <p><strong>⚠️ Avoid:</strong> Heavily padded puff sleeves and boatneck tops.</p>
                <div class="script-box"><strong>Power Formula:</strong> Fluid drapey wrap blouse + wide-leg palazzo trousers + delicate minimalist drop earrings.</div>
            </div>
            """, unsafe_allow_html=True)

    with tab_cap:
        st.markdown("### The 15-Piece French-Chic Capsule Wardrobe")
        st.write("Own these 15 timeless, high-mileage essentials to create 50+ effortless outfits:")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            - 🧥 **The Camel Wool Coat** *(Instant luxury layer)*
            - 👔 **The Crisp White Cotton Shirt** *(Slightly oversized)*
            - 👖 **Charcoal High-Rise Trousers** *(Day-to-night staple)*
            - 👗 **Little Black Bias Slip Dress** *(Layer or wear solo)*
            - 💼 **The Tailored Black Blazer** *(Boardroom authority)*
            """)
        with c2:
            st.markdown("""
            - 👖 **Straight-Leg Dark Wash Denim** *(No rips; elegant)*
            - 🧶 **Crewneck Cashmere Knit** *(Oatmeal or camel)*
            - 🧥 **Classic Double-Breasted Trench** *(Water-resistant)*
            - 🎽 **Silk Camisole (Champagne/Black)** *(Perfect base)*
            - 👞 **Black Leather Loafers** *(Chic walking comfort)*
            """)
        with c3:
            st.markdown("""
            - 👠 **Pointed-Toe Black/Nude Pumps** *(7cm poise)*
            - 👟 **Clean White Leather Sneakers** *(Weekend luxury)*
            - 👜 **Structured Leather Handbag** *(Minimal logos)*
            - ⌚ **Gold Watch & Hoop Earrings** *(Signature shine)*
            - 🧣 **Silk Square Scarf** *(Tie on bag, neck, or hair)*
            """)

    with tab_look:
        st.markdown("### Curated Occasion Blueprints")
        oc1, oc2 = st.columns(2)
        with oc1:
            st.markdown("""
            <div class="aura-card">
                <span class="badge-pill">01. Power Career Meeting</span>
                <h5>The Sharp Authority</h5>
                <p style="font-size: 0.85rem; color: #555;">Double-breasted camel blazer + ivory silk camisole + charcoal high-waisted wide-leg trousers + pointed block heels + structured tote.</p>
            </div>
            
            <div class="aura-card">
                <span class="badge-pill">02. Casual French-Chic</span>
                <h5>Effortless Café Ease</h5>
                <p style="font-size: 0.85rem; color: #555;">Breton striped boatneck top or crisp white button-down + straight-leg dark wash denim + black leather loafers + trench coat over shoulders.</p>
            </div>
            """, unsafe_allow_html=True)
        with oc2:
            st.markdown("""
            <div class="aura-card">
                <span class="badge-pill">03. Romantic Evening / Dinner</span>
                <h5>The Velvet Mystery</h5>
                <p style="font-size: 0.85rem; color: #555;">Bias-cut slip dress in champagne, olive, or noir + draped oversized wool coat + dainty gold chain + minimal kitten heels + signature amber fragrance.</p>
            </div>
            
            <div class="aura-card">
                <span class="badge-pill">04. Weekend Elevated Luxe</span>
                <h5>Clean Girl Quiet Luxury</h5>
                <p style="font-size: 0.85rem; color: #555;">Oatmeal cashmere knit sweater + ivory pleated trousers + sleek minimalist white retro sneakers + tortoise-shell sunglasses + sleek low bun.</p>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# 8. TAB 4: LOOKS, SKINCARE & POISE
# ==============================================================================

elif menu == "✨ Looks, Skincare & Poise":
    st.markdown("## ✨ Looks, Radiance & Physical Poise")
    st.write("High-maintenance habits that keep you effortlessly low-maintenance daily.")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("### 🧴 The 'Thin-to-Thick' Skincare Master Order")
        st.markdown("""
        <div class="aura-card">
            <span class="badge-pill">Step 1: Gentle / Double Cleanse</span>
            <p style="font-size: 0.85rem; color: #555;">Use an oil cleanser at night to dissolve SPF and makeup, followed by a gentle hydrating water-based gel cleanser.</p>
        </div>
        <div class="aura-card">
            <span class="badge-pill">Step 2: Hydrating Toner / Essence</span>
            <p style="font-size: 0.85rem; color: #555;">Apply hyaluronic acid toner onto slightly damp skin so it binds moisture into the skin barrier.</p>
        </div>
        <div class="aura-card">
            <span class="badge-pill">Step 3: Active Treatment Serums</span>
            <p style="font-size: 0.85rem; color: #555;">Vitamin C in the morning for radiance and pollution defense; Retinol or Peptides at night for collagen and smooth texture.</p>
        </div>
        <div class="aura-card">
            <span class="badge-pill">Step 4: Ceramide Moisturizer</span>
            <p style="font-size: 0.85rem; color: #555;">Locks in hydration and protects the lipid barrier against dullness and irritation.</p>
        </div>
        <div class="aura-card" style="border: 2px solid #C77D87;">
            <span class="badge-pill" style="background: #C77D87; color: white;">Step 5: Non-Negotiable SPF 50+</span>
            <p style="font-size: 0.85rem; color: #555;">90% of premature aging and discoloration is UV-induced. Apply rain or shine every single morning.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_s2:
        st.markdown("### 👑 Posture, Walking & Scent Stacking")
        st.markdown("""
        <div class="aura-card">
            <h5>1. The Invisible Crown Line</h5>
            <p style="font-size: 0.85rem; color: #555;">Imagine a golden thread pulling gently upward from the crown of your head. Roll shoulders up, back, and gently downward away from your ears.</p>
        </div>
        
        <div class="aura-card">
            <h5>2. Grounded Hip Movement</h5>
            <p style="font-size: 0.85rem; color: #555;">Lead your stride from your hips rather than leaning with your shoulders. Keep your chin parallel to the ground; never look down at your feet while walking into a room.</p>
        </div>
        
        <div class="aura-card">
            <h5>3. The Scent Stacking Ritual</h5>
            <p style="font-size: 0.85rem; color: #555;">Apply scented body lotion immediately out of the shower while skin is damp. Spray signature eau de parfum on pulse points (collarbones, behind ears, wrists) and a gentle mist on your hairbrush.</p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 9. TAB 5: MAIA AI THERAPIST & WELLNESS GUIDE
# ==============================================================================

elif menu == "💖 Maia: AI Therapist & Guide":
    st.markdown("## 💖 Maia: AI Emotional Sanctuary")
    st.write("Your warm, safe, non-judgmental space for emotional reframing, confidence, and self-love.")
    
    st.caption("💛 *Maia is an AI supportive mentor and emotional wellness guide, not a licensed medical therapist. In emergencies, please dial your local crisis lifeline (e.g., 988).*")
    
    # 4-7-8 Breathing Guide Expander
    with st.expander("🕊️ Feeling Anxious? Click for 3-Minute 4-7-8 Breathing Exercise"):
        st.markdown("""
        **4-7-8 Nervous System Reset:**
        1. **Inhale quietly** through your nose for **4 seconds**.
        2. **Hold your breath** gently for **7 seconds**.
        3. **Exhale completely** through your mouth with a soft whoosh for **8 seconds**.
        *Repeat 4 times to stimulate the vagus nerve and bring your heart rate to peace.*
        """)
    
    # Initialize Chat History
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "Hello beautiful soul. 🌸 I am **Maia**, your personal emotional wellness companion. "
                           "Whether you need to untangle self-doubt, reframe a stressful day, practice speaking up with poise, "
                           "or remind yourself of your extraordinary worth—I am right here with you. How is your heart feeling today?"
            }
        ]

    # Quick Prompt Pills
    st.markdown("**Quick Topics:**")
    qp_col1, qp_col2, qp_col3, qp_col4 = st.columns(4)
    with qp_col1:
        if st.button("🌊 Feeling overwhelmed"):
            st.session_state.selected_quick_prompt = "I am feeling so overwhelmed and not good enough today."
    with qp_col2:
        if st.button("🚫 Stop people-pleasing"):
            st.session_state.selected_quick_prompt = "How do I stop people-pleasing and learn to say NO gracefully?"
    with qp_col3:
        if st.button("💼 Imposter syndrome"):
            st.session_state.selected_quick_prompt = "I have imposter syndrome about my career and success."
    with qp_col4:
        if st.button("🪞 Mirror meditation"):
            st.session_state.selected_quick_prompt = "Can you guide me through a 2-minute self-love mirror affirmation?"

    # Display Chat History
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"], avatar="👑" if msg["role"] == "user" else "🌸"):
            st.markdown(msg["content"])

    # Chat Input Handling
    default_prompt = st.session_state.pop("selected_quick_prompt", None)
    user_input = st.chat_input("Pour your heart out to Maia...") or default_prompt
    
    if user_input:
        # Display user message
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👑"):
            st.markdown(user_input)
            
        # Generate assistant response
        with st.chat_message("assistant", avatar="🌸"):
            with st.spinner("Maia is reflecting with you..."):
                response = query_ai_therapist(user_input, st.session_state.chat_messages)
                st.markdown(response)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})

    if st.button("🗑️ Reset Conversation"):
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "Hello beautiful soul. 🌸 I am **Maia**. How is your heart feeling today?"
            }
        ]
        st.rerun()

# ==============================================================================
# 10. TAB 6: DAILY HABITS & JOURNAL
# ==============================================================================

else:
    st.markdown("## 📖 Daily Self-Love Rituals & Journal")
    st.write("Small, intentional daily rituals to fortify your self-respect and feminine sovereignty.")
    
    col_h1, col_h2 = st.columns(2)
    
    with col_h1:
        st.markdown("### 👑 Today's Queen Habits")
        h1 = st.checkbox("💧 Drank 2.5L water with lemon or electrolytes")
        h2 = st.checkbox("🧴 Completed morning and evening skincare + SPF 50+")
        h3 = st.checkbox("🧘‍♀️ Checked posture & practiced crown alignment")
        h4 = st.checkbox("📚 Read 10 pages of personal growth, finance, or poetry")
        h5 = st.checkbox("🛡️ Practiced 1 boundary without apologizing")
        h6 = st.checkbox("🪞 Spoke 3 loving truths to myself in the mirror")
        
        habits_done = sum([h1, h2, h3, h4, h5, h6])
        st.progress(habits_done / 6.0)
        st.write(f"**Progress:** {habits_done}/6 Habits Completed Today! {'🌟 You are radiating!' if habits_done == 6 else ''}")

    with col_h2:
        st.markdown("### ✍️ Self-Love Mirror Journal")
        st.write("*Prompt: What is one standard you are no longer willing to lower for anyone, and why?*")
        
        journal_text = st.text_area(
            "Your Private Journal Reflection:",
            height=200,
            placeholder="Write freely here. This is your personal sacred space..."
        )
        
        if journal_text:
            st.download_button(
                label="📥 Download Journal Entry (.txt)",
                data=f"AURA Sanctuary Journal — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{journal_text}",
                file_name=f"aura_journal_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

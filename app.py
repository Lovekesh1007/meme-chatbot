import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Meme Chatbot", layout="wide")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# ================== CSS ==================
st.markdown("""
<style>
body {
    background: #0e1117;
}

.bubble-user {
    background: linear-gradient(135deg, #007bff, #00c6ff);
    color: white;
    padding: 12px 16px;
    border-radius: 16px;
    max-width: 65%;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.bubble-ai {
    background: #262730;
    color: white;
    padding: 12px 16px;
    border-radius: 16px;
    max-width: 65%;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.stButton>button {
    border-radius: 10px;
    background: linear-gradient(135deg,#ff4b4b,#ff7a7a);
    color: white;
    border: none;
}

.title {
    text-align:center;
    font-size:40px;
    font-weight:700;
}
</style>
""", unsafe_allow_html=True)

# ================== SESSION ==================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ================== SIDEBAR ==================
st.sidebar.header("⚙️ Settings")

tone = st.sidebar.selectbox(
    "Choose tone:",
    ["Funny 😂", "Savage 😈", "Dark 🖤"]
)

style = st.sidebar.selectbox(
    "Caption Style",
    ["Relatable", "Roast", "Motivational", "Dark Humor"]
)

length = st.sidebar.slider("Caption Length", 20, 120, 60)

if st.sidebar.button("🔥 Try Trending Idea"):
    st.session_state.input = "when teacher says surprise test"

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []

# ================== TITLE ==================
st.markdown("<div class='title'>😂 AI Meme Chatbot</div>", unsafe_allow_html=True)

# ================== CHAT DISPLAY ==================
chat_container = st.container()

with chat_container:
    for chat in st.session_state.chat_history:

        # USER
        st.markdown(f"""
        <div style='display:flex; justify-content:flex-end; margin-bottom:10px'>
            <div class="bubble-user">👤 {chat['user']}</div>
        </div>
        """, unsafe_allow_html=True)

        # AI
        for c in chat["response"]:
            if c.strip():
                st.markdown(f"""
                <div style='display:flex; justify-content:flex-start; margin-bottom:8px'>
                    <div class="bubble-ai">🤖 {c}</div>
                </div>
                """, unsafe_allow_html=True)

# ================== INPUT ==================
user_input = st.text_input("💬 Type your message...", key="input")

col1, col2, col3 = st.columns([4,1,1])

with col2:
    send = st.button("➤")

with col3:
    regen = st.button("🔁")

# ================== GENERATE ==================
if (send or regen) and user_input:

    prompt = f"""
You are a top-tier meme creator who writes viral captions for Instagram, Reddit, and Gen-Z audiences.

Your goal is to create captions that feel ORIGINAL, FUNNY, RELATABLE, and SHARE-WORTHY.

Context:
Topic: {user_input}
Tone: {tone}
Style: {style}

Strict Instructions:
- Generate EXACTLY 3 captions
- Each caption must feel like a real viral meme (not generic)
- Use Gen-Z humor, sarcasm, exaggeration, or irony
- Prefer formats like:
  • "POV:"
  • "When you..."
  • "That moment when..."
- Add relevant emojis naturally (not forced)
- Make captions punchy, short, and impactful
- Avoid repetition between captions
- Avoid boring or safe lines
- Make at least ONE caption slightly savage or unexpected
- Keep each caption under {length} characters

Quality Boost Rules:
- Think like a meme page admin with millions of followers
- Use real-life relatable situations
- Add twist or punchline at the end
- Make captions scroll-stopping

Output format:
1. caption
2. caption
3. caption
"""

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_text = response.choices[0].message.content

        captions = [c.strip() for c in raw_text.split("\n") if c.strip()]

        # SAVE CHAT
        st.session_state.chat_history.append({
            "user": user_input,
            "response": captions
        })

        # DOWNLOAD BUTTON
        st.download_button(
            "📥 Download Captions",
            "\n".join(captions),
            file_name="captions.txt"
        )

        st.rerun()

    except Exception as e:
        st.error(e)
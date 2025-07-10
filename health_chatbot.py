import streamlit as st
from transformers import pipeline
from streamlit_chat import message
import pandas as pd
import matplotlib.pyplot as plt
from deep_translator import GoogleTranslator

# 🧠 GPT setup
generator = pipeline("text-generation", model="gpt2")
def generate_ai_reply(prompt_text):
    result = generator(prompt_text, max_length=100, do_sample=True, num_return_sequences=1)
    return result[0]['generated_text']

# 🌍 Translation
def translate_hindi(text):
    return GoogleTranslator(source='auto', target='hi').translate(text)

# 🎨 UI settings
st.set_page_config(page_title="AI Health Chatbot", page_icon="🩺", layout="wide")
st.markdown("""
    <style>
    .main {background-color: #f9f9f9;}
    h1 {color:#e67e22;}
    div.stTextInput > label { font-size:18px; color:#2c3e50; font-weight:600; }
    </style>
""", unsafe_allow_html=True)

# 📘 Title
st.title("🩺 AI Health Chatbot with GPT-style Responses")

# 💬 User input
user_input = st.text_input("🧠 What are your symptoms or health questions?")

# 📊 Wellness chart
with st.expander("📈 Daily Health Snapshot"):
    categories = ["Water (L)", "Sleep (hrs)", "Steps"]
    values = [2.5, 7, 5200]
    fig, ax = plt.subplots()
    ax.bar(categories, values, color=['#27ae60', '#3498db', '#e67e22'])
    st.pyplot(fig)

# 📋 FAQs
with st.expander("📋 Health FAQs"):
    faq = pd.DataFrame({
        "Question": ["What to eat during typhoid?", "Remedy for period cramps?", "Best food for migraines?"],
        "Answer": ["Boiled food, coconut water, avoid spices.",
                   "Warm compress, yoga, flaxseed.",
                   "Eggs, spinach, avoid caffeine."]
    })
    keyword = st.text_input("🔍 Search symptom keyword:")
    if keyword:
        results = faq[faq["Question"].str.contains(keyword, case=False)]
        for _, row in results.iterrows():
            message(f"**Q:** {row['Question']}", is_user=False)
            message(f"**A:** {row['Answer']}", is_user=False)

# 🩺 Symptom advice dictionary
health_issues = {
    "fever": ["🌡️ Use tulsi tea & hydration.", "🍲 Eat boiled veggies, light soups."],
    "migraine": ["🔮 Try peppermint oil.", "🥦 Eat spinach, avoid bright lights."],
    "period cramps": ["🩸 Use warm pad, yoga.", "🧘 Drink turmeric milk, flaxseed."],
    "nausea": ["🤢 Sip ginger tea slowly.", "🍞 Eat toast, avoid oily food."],
    "pcos": ["🌸 Eat nuts & flaxseed.", "🚫 Avoid processed sugar."],
    "diabetes": ["🧬 Bitter gourd, cinnamon, oats.", "🚶 Walk post meals daily."],
    "acidity": ["🍋 Avoid citrus and spicy food.", "🌿 Try fennel seeds or chamomile tea."],
    "constipation": ["🥣 Eat fiber-rich foods.", "🚶 Walk daily and drink warm water."],
    "cold": ["🌿 Steam inhalation.", "🍯 Tulsi-honey tea and rest."],
    "fatigue": ["🛏️ Sleep 7–8 hrs.", "🥗 Eat magnesium-rich foods."],
    "anemia": ["🥩 Dates, jaggery, spinach.", "💊 Take vitamin C for iron absorption."],
    "eye pain": ["👁️ Use 20-20-20 screen rule.", "🥕 Eat carrots and omega-3s."],
    "headache": ["💆 Massage with lavender oil.", "🥤 Stay hydrated and avoid screens."],
    "stomach ache": ["🍲 Light meals: banana, rice.", "🌿 Sip ajwain or ginger tea."],
    "typhoid": ["🥣 Boiled food only.", "🚫 Avoid dairy and spicy items."],
    "dengue": ["🩸 Papaya leaf extract.", "🍶 ORS and coconut water."],
    "body pain": ["🛁 Warm bath with Epsom salt.", "🧘 Light stretch or walk."],
    "menstrual fatigue": ["🌙 Rest and eat iron-rich food.", "🍵 Chamomile or ginger tea."],
    "vomiting": ["🍋 Lemon water with salt.", "🫖 Ginger-honey tea."],
    "allergy": ["🌬️ Saline nasal spray.", "🥗 Avoid triggers like nuts/dust."]
}

# 💡 Match user input
if user_input:
    message(user_input, is_user=True)
    symptoms = user_input.lower()
    is_severe = any(word in symptoms for word in ["severe", "unbearable", "very bad"])

    found = False
    matched_tips = []
    for symptom, tips in health_issues.items():
        if symptom in symptoms:
            found = True
            matched_tips = tips
            for tip in tips:
                message(f"{tip}", is_user=False)
            if is_severe:
                message("⚠️ This may require medical attention. Please consult a doctor.", is_user=False)
            break  # Prevent GPT fallback if match found

    if not found:
        gpt_reply = generate_ai_reply(f"A patient says: '{user_input}'. Give some gentle health suggestions.")
        message("🤖 GPT-style Advice:", is_user=False)
        message(gpt_reply, is_user=False)

        with st.expander("🌐 Translate GPT Advice to Hindi"):
            translated = translate_hindi(gpt_reply)
            message(f"🇮🇳 {translated}", is_user=False)
    else:
        with st.expander("🌐 Translate First Tip to Hindi"):
            translated = translate_hindi(matched_tips[0])
            message(f"🇮🇳 {translated}", is_user=False)

# 🛡️ Disclaimer
st.caption("🛡️ This chatbot is for educational use only and does not replace advice from licensed healthcare professionals.")

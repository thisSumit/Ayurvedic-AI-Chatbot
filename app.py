import streamlit as st
import os
import requests

MISTRAL_API_KEY = st.secrets.get("MISTRAL_API_KEY", os.getenv("MISTRAL_API_KEY"))
if not MISTRAL_API_KEY:
    st.error("⚠️ API key is missing! Please set MISTRAL_API_KEY in Streamlit secrets or environment variables.")
    st.stop()

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "ft:ministral-3b-latest:a478ba39:20250816:659c4aac"

def get_ayurvedic_remedy(symptoms):
    prompt = f"""
    If user are asking general questions like hi, hello other than diseases and feelings give them feedback as per Normal people and suggest them to ask only about their health issues.
You are an Ayurvedic health advisor.
Symptoms: {symptoms}

Provide:
1. Ayurvedic remedies (mention herbs, home treatments, and dosages if possible)
2. Daily precautions
3. Dietary recommendations
4. Lifestyle changes
5. Disclaimer that this is not a substitute for professional medical advice.
"""
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "system", "content": "You are an Ayurvedic health advisor."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1024,
        "temperature": 1.0
    }
    try:
        resp = requests.post(MISTRAL_API_URL, headers=headers, json=data)
        resp.raise_for_status()
        result = resp.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Unable to fetch remedies. Error: {str(e)}"

st.set_page_config(page_title="Ayurvedic AI Chatbot", page_icon="🌿")
st.title("🌿 Ayurvedic AI Chatbot")
st.write("Describe your symptoms below to receive **Ayurvedic remedies & precautions**.")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_area("📝 Describe your symptoms:")


if st.button("💡 Get Remedy"):
    if user_input.strip():
        with st.spinner("Fetching Ayurvedic remedy..."):
            result = get_ayurvedic_remedy(user_input)
            st.write(result)
        st.session_state.history.append((user_input, result))
    else:
        st.warning("⚠️ Please enter your symptoms.")


if st.session_state.history:
    st.markdown("---")
    st.subheader("💬 Conversation History")
    for user_msg, ai_msg in reversed(st.session_state.history):
        st.markdown("**User:**")
        st.markdown(f"> {user_msg}")
        st.markdown("**Doctor AI:**")
        st.markdown(f"> {ai_msg}")
        st.markdown("---")

st.markdown("---")
st.markdown("⚠️ *This AI Doctor provides general Ayurvedic suggestions. Please consult a qualified practitioner before following any remedy.*")
st.markdown("💻 Developed by **Sumit Karanjekar**")
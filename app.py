import streamlit as st
import os
import google.generativeai as genai


API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
if not API_KEY:
    st.error("⚠️ API key is missing! Please set GOOGLE_API_KEY in Streamlit secrets or environment variables.")
    st.stop()

genai.configure(api_key=API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

MODEL_ID = "tunedModels/ayurvedicaisymptomdataset500-x62zcg30yiy"
model = genai.GenerativeModel(MODEL_ID)

def get_ayurvedic_remedy(symptoms):
    try:
        prompt = f"""
You are an Ayurvedic health advisor.
Symptoms: {symptoms}

Provide:
1. Ayurvedic remedies (mention herbs, home treatments, and dosages if possible)
2. Daily precautions
3. Dietary recommendations
4. Lifestyle changes
5. Disclaimer that this is not a substitute for professional medical advice.
"""
        response = model.generate_content(prompt)
        return response.text.strip()
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
        st.session_state.history.append(("🧑 You", user_input))
        st.session_state.history.append(("🤖 AI Doctor", result))
    else:
        st.warning("⚠️ Please enter your symptoms.")

if st.session_state.history:
    st.markdown("---")
    st.subheader("💬 Conversation")
    for role, message in st.session_state.history:
        st.markdown(f"**{role}:** {message}")

st.markdown("---")
st.markdown("⚠️ *This AI Doctor provides general Ayurvedic suggestions. Please consult a qualified practitioner before following any remedy.*")
st.markdown("💻 Developed by **Amit Anand Sumit**")

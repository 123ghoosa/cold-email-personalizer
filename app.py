import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load .env file with your OpenAI API key
load_dotenv()

st.title("🎯 Cold Email Personalizer (MVP)")

# Input form
with st.form("personalize_form"):
    name = st.text_input("Name")
    title = st.text_input("Job Title")
    company = st.text_input("Company Name")
    bio = st.text_area("LinkedIn Bio or Headline")
    activity = st.text_area("Recent Activity (Post, Event, News)", "")
    submitted = st.form_submit_button("Generate Openers")

if submitted:
    with st.spinner("Generating personalized openers..."):
        # Your GPT-4o personalization prompt
        system_msg = """
You are a B2B sales expert writing high-converting cold email openers.

Your job is to take basic information about a prospect and generate 1–2 personalized opening lines that could be used at the start of a cold outreach email.

Guidelines:
- Start with their *role*, *company*, or *past achievement*.
- Be concise (1–2 sentences MAX).
- Be specific. Refer to what the prospect *actually does*, not generic praise.
- Avoid cliches like “Hope you're doing well” or “I came across your profile”.

Tone: friendly and professional.
"""

        user_data = {
            "name": name,
            "title": title,
            "company": company,
            "bio": bio,
            "recent_activity": activity,
        }

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": str(user_data)},
                ],
                temperature=0.7,
                max_tokens=250,
            )
            output = response.choices[0].message.content
            st.success("Here are your openers:")
            st.write(output)

        except Exception as e:
            st.error(f"Something went wrong: {e}")

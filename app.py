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
You are helping write highly personalized cold email openers for a B2B founder reaching out to potential clients. These openers should be short, warm, and show that you truly read and understood the recipient’s LinkedIn profile and recent activity.

Use the person’s name, job title, company, bio, and recent post or activity to personalize a 1–2 sentence opener. Avoid fluff or praise that sounds generic. Focus on relevance, shared curiosity, or something timely. Write like a founder who respects the other person’s time.

Respond only with the opener line.

INPUT EXAMPLE:

Name: Taylor Smith  
Job Title: Growth Lead at Zywa  
Bio: 8+ years building growth, acquisition, and funnel ops for B2B and AI-native startups. Fluent in HubSpot, Clearbit, GA.  
Recent Activity: Excited to lead global growth for a voice-AI enterprise software company.

OUTPUT:
Loved seeing your move to Zywa — seems like a great fit with your background scaling growth for B2B and AI-native startups. Curious how you’re thinking about voice AI for enterprise!
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

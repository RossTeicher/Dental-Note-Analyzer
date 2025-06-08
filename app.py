
import streamlit as st
from openai import OpenAI
import os

# Set OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Dental Note Generator")

user_input = st.text_area("Enter clinical findings or notes:")

if st.button("Generate Note"):
    if user_input.strip() == "":
        st.warning("Please enter some input.")
    else:
        with st.spinner("Generating note..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates dental clinical notes."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success("Note generated!")
            st.text_area("Generated Note", response.choices[0].message.content, height=200)

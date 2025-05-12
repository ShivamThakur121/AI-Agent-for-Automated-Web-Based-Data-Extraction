import streamlit as st

def get_user_prompt():
    return st.text_input("Enter your query (e.g. Get the email of {company})")
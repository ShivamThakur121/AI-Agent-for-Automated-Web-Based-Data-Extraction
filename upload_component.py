import streamlit as st
import pandas as pd
from app.services.file_handler import read_google_sheet

def upload_data():
    print("Inside upload_component.py")
    file = st.file_uploader("Upload CSV file", type=["csv"])
    sheet_url = st.text_input("Or enter a public Google Sheet URL")

    if file:
        df = pd.read_csv(file)
        return df, df.columns.tolist()
    elif sheet_url:
        df = read_google_sheet(sheet_url)
        return df, df.columns.tolist()
    return None, []

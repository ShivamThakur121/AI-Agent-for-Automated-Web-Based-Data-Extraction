import streamlit as st
import pandas as pd
# from google import genai
import google.generativeai as genai

# --------------------- CONFIGURE GEMINI ---------------------
API_KEY = "AIzaSyCCB2-Aovw6ObOGM5863S0muIVgSXRk8-U"  # 🔐 Replace with your key 

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("❌ Failed to initialize Gemini client. Check your API key.")
    st.exception(e)
    st.stop()

# --------------------- STREAMLIT UI ---------------------
st.set_page_config(page_title="Gemini CSV Analyzer", layout="centered")
st.title("🔍 Gemini CSV Insight Extractor")
st.markdown("Upload a CSV file, select a column, and ask Gemini AI to analyze the data.")

# Upload CSV
uploaded_file = st.file_uploader("📄 Upload a CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ CSV loaded successfully.")
        st.dataframe(df.head())

        # Select column
        columns = df.columns.tolist()
        selected_column = st.selectbox("Select a column to analyze:", columns)

        # User prompt
        user_prompt = st.text_input(
            "🧠 Enter your question or instruction:",
            placeholder="e.g., Summarize the companies listed below"
        )

        if st.button("🔎 Perform Web Search"):
            try:
                if selected_column not in df.columns:
                    st.warning("Selected column is not in the DataFrame.")
                    st.stop()

                # Clean and format data
                data_values = df[selected_column].dropna().astype(str).tolist()
                entity_string = "\n".join(data_values)
                full_prompt = f"{user_prompt.strip()}\n\nData:\n{entity_string.strip()}"

                with st.spinner("💬 Sending request to Web Search..."):
                    model = genai.GenerativeModel("gemini-1.5-flash")  # Use available model name
                    response = model.generate_content(full_prompt)

                    # Post-process response to remove extra formatting artifacts
                    cleaned_response = response.text.replace("*", "").replace("•", "-").strip()

                    st.success("✅ Gemini responded!")
                    st.subheader("📄 Gemini's Response")
                    st.text_area("Response", value=cleaned_response, height=400)

            except Exception as e:
                st.error("❌ Error during Gemini API call.")
                st.exception(e)

    except Exception as e:
        st.error("❌ Failed to read CSV file.")
        st.exception(e)
else:
    st.info("👆 Please upload a CSV file to get started.")


import streamlit as st
import pandas as pd
import google.generativeai as genai
import requests

# --------------- CONFIGURATION ---------------
GEMINI_API_KEY = "GEMINI_API_KEY"
SERPAPI_KEY = "SERPAPI_KEY"

try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error("❌ Failed to initialize Gemini client.")
    st.exception(e)
    st.stop()

# --------------- SEARCH FUNCTION ---------------
def search_web(entity, prompt):
    query = prompt.replace("{company}", entity)
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google"
    }
    response = requests.get("https://serpapi.com/search", params=params)
    return response.json().get("organic_results", [])

# --------------- STREAMLIT UI ---------------
st.set_page_config(page_title="Gemini Company Analyzer", layout="centered")
st.title("🏢 Company Insight Extractor")
st.markdown("Upload your CSV, select a column, and get real-time company info.")

uploaded_file = st.file_uploader("📄 Upload a CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ CSV loaded successfully.")
        st.dataframe(df.head())

        # Select column
        columns = df.columns.tolist()
        selected_column = st.selectbox("🧠 Select the column with company names:", columns)

        # User input
        user_prompt = st.text_input(
            "🔍 Enter your question (use {company} as placeholder):",
            placeholder="e.g., What is the age of {company}?"
        )

        if st.button("💡 Analyze with Gemini"):
            try:
                # Step 1: Extract company names
                company_list = df[selected_column].dropna().astype(str).unique().tolist()
                short_list = company_list[:5]  # Limit to avoid long prompt

                # Step 2: Perform search
                search_results = []
                for company in short_list:
                    results = search_web(company, user_prompt)
                    snippets = [r.get("snippet", "") for r in results]
                    joined = "\n".join(snippets)
                    search_results.append(f"### {company}\n{joined}")

                # Step 3: Create final prompt
                final_prompt = f"""
Use the following search results to answer this question:

Question: {user_prompt}

Search Results:
{"".join(search_results)}
"""

                # Step 4: Ask Gemini
                with st.spinner("💬 Asking Gemini..."):
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(final_prompt)
                    output = response.text.strip()

                st.success("✅ Gemini responded!")
                st.subheader("📄 Gemini's Response")
                st.text_area("Response", value=output, height=500)

            except Exception as e:
                st.error("❌ Error during Gemini + search.")
                st.exception(e)

    except Exception as e:
        st.error("❌ Could not read the CSV.")
        st.exception(e)

else:
    st.info("👆 Please upload a CSV file to get started.")

import streamlit as st
import pandas as pd

def display_results(results):
    df = pd.DataFrame(results)
    st.write("## Extracted Results")
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False), file_name="extracted_data.csv", mime="text/csv")

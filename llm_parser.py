import pandas as pd
from google import genai

# --- Set up Gemini Client ---
API_KEY = "AIzaSyCCB2-Aovw6ObOGM5863S0muIVgSXRk8-U"
client = genai.Client(api_key=API_KEY)

# --- Read Google Sheet ---
def read_google_sheet(url):
    if "docs.google.com/spreadsheets" not in url:
        raise ValueError("Not a valid Google Sheet URL.")

    try:
        if "/edit#gid=" in url:
            base, gid = url.split("/edit#gid=")
            sheet_id = base.split("/d/")[1]
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        else:
            raise ValueError("URL must contain '/edit#gid=' format.")
        
        df = pd.read_csv(csv_url)
        return df
    except Exception as e:
        raise RuntimeError(f"Failed to read Google Sheet: {e}")

# --- Prepare prompt for Gemini ---
def prepare_gemini_prompt(df):
    print("\nAvailable columns:", list(df.columns))
    column_name = input("Enter the column name to extract values from: ")

    if column_name not in df.columns:
        raise ValueError("Invalid column name.")

    values_list = df[column_name].dropna().astype(str).tolist()
    column_string = "\n".join(values_list)

    user_query = input("Enter your query or instruction (e.g., 'Summarize these companies'): ")

    full_prompt = f"{user_query}\n\nData:\n{column_string}"
    return full_prompt

# --- Send prompt to Gemini ---
def ask_gemini(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error using Gemini API: {e}"

# --- Main process ---
def main():
    url = input("Enter the public Google Sheet URL: ")
    df = read_google_sheet(url)

    gemini_prompt = prepare_gemini_prompt(df)
    print("\n--- Prompt sent to Gemini ---\n")
    print(gemini_prompt)

    print("\n--- Gemini Response ---\n")
    result = ask_gemini(gemini_prompt)
    print(result)

if __name__ == "__main__":
    main()

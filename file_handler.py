import pandas as pd

def process_file():
    # Function implementation
    print("ram")
    pass

def read_google_sheet(url):
    """
    Converts a public Google Sheet URL to a direct CSV download link,
    then loads it into a pandas DataFrame.
    """
    if "https://docs.google.com/spreadsheets/d/1AbC123abcD456efG7HIjkLmNOPq8rsT9/edit#gid=" in url:
        csv_url = url.replace("https://docs.google.com/spreadsheets/d/1AbC123abcD456efG7HIjkLmNOPq8rsT9/edit#gid=0", "https://docs.google.com/spreadsheets/d/1AbC123abcD456efG7HIjkLmNOPq8rsT9/export?format=csv&gid=0")
    else:
        raise ValueError("Invalid Google Sheet URL format.")
    
    try:
        df = pd.read_csv(csv_url)
        return df
    except Exception as e:
        raise RuntimeError(f"Failed to read Google Sheet: {e}")
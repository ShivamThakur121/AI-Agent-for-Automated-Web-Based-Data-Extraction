import pandas as pd
from app.services.file_handler import read_google_sheet

def test_read_google_sheet():
    url = "https://docs.google.com/spreadsheets/d/e/.../edit#gid=0"
    assert read_google_sheet(url).shape[0] > 0
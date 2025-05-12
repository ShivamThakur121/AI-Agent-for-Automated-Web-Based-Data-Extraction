# AI Agent for Data Extraction

This project builds an AI Agent that:
- Searches the web using a query template
- Uses LLM to extract structured data
- Outputs a downloadable CSV or connected Google Sheet

## Features
- CSV/Google Sheets input
- Query-based extraction
- GPT-based summarization

## Setup
```bash
pip install -r requirements.txt
```
Create a `.env` file using `.env.example` and add your API keys.

Run the app:
```bash
streamlit run main.py
```

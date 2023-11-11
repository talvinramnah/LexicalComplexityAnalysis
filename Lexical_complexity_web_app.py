import requests
from beautifulsoup4 import BeautifulSoup
import openai
import streamlit as st
import pandas as pd
# Global list to store analysis results
analysis_results = []
# Function to extract text from a URL
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            text = ' '.join([p.get_text() for p in paragraphs])
            return text
        else:
            print(f"Failed to retrieve {url}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Function to analyze CEFR level and lexical complexity using OpenAI

def analyze_text_with_openai(text, openai_api_key):
    try:
        openai.api_key = openai_api_key
        prompt = f"Provide a lexical complexity score on a scale from 0 to 100 for the following text:\n{text}"
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=60,
            temperature=0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"An error occurred with OpenAI: {e}")
        return "Error"

# Replace with your actual OpenAI API key
OPENAI_API_KEY = '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'

if 'analysis_results' not in st.session_state:
    st.session_state['analysis_results'] = []

st.title('AI Lexical Complexity Analyzer')
st.subheader('Enter the URL of an article to analyze its lexical complexity')

user_url = st.text_input("Article URL:")

if st.button("Analyze"):
    article_text = extract_text_from_url(user_url)
    if article_text:
        lexical_complexity_score = analyze_text_with_openai(article_text, OPENAI_API_KEY)
        if lexical_complexity_score.isdigit():
            article_title = BeautifulSoup(requests.get(user_url).content, 'html.parser').title.string
            st.session_state['analysis_results'].append({
                "Article Title": article_title,
                "Article URL": user_url,
                "Lexical Complexity Score": lexical_complexity_score
            })
        else:
            st.error(f"Failed to analyze text. Reason: {lexical_complexity_score}")
    else:
        st.error("Failed to retrieve article.")

# Display the entire list of results
if st.session_state['analysis_results']:
    st.subheader("All Analysis Results")
    st.table(pd.DataFrame(st.session_state['analysis_results']))
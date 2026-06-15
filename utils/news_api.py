import requests
import streamlit as st

BASE_URL = "https://newsapi.org/v2/top-headlines"


@st.cache_data(ttl=300)
def fetch_news(country, category, keyword, page_size):

    api_key = st.secrets["NEWS_API_KEY"]

    params = {
        "apiKey": api_key,
        "country": country,
        "category": category,
        "pageSize": page_size
    }

    if keyword:
        params["q"] = keyword

    response = requests.get(BASE_URL, params=params)

    response.raise_for_status()

    return response.json()
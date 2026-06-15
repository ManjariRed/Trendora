import streamlit as st
import pandas as pd
from datetime import datetime

from utils.news_api import fetch_news
st.set_page_config(
    page_title="News Explorer",
    page_icon="📰",
    layout="wide"
)
st.title("📰 Advanced News Explorer")

st.write(
    "Explore the latest headlines from around the world."
)
countries = {
    "India": "in",
    "United States": "us",
    "United Kingdom": "gb",
    "Australia": "au",
    "Canada": "ca",
    "Germany": "de",
    "France": "fr",
    "Japan": "jp"
}

categories = [
    "general",
    "business",
    "entertainment",
    "health",
    "science",
    "sports",
    "technology"
]

st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Country",
    list(countries.keys())
)

category = st.sidebar.selectbox(
    "Category",
    categories
)

keyword = st.sidebar.text_input(
    "Keyword Search"
)

page_size = st.sidebar.slider(
    "Number of Articles",
    5,
    50,
    10
)

search = st.sidebar.button("Fetch News")
if search:

    with st.spinner("Fetching news..."):

        try:
            data = fetch_news(
                countries[country],
                category,
                keyword,
                page_size
            )

            articles = data["articles"]

        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()
            if not articles:
    st.warning("No articles found.")
    else:
    st.success(
        f"Found {len(articles)} articles."
    )
    sources = {}

for article in articles:
    source = article["source"]["name"]

    sources[source] = (
        sources.get(source, 0) + 1
    )

col1, col2, col3 = st.columns(3)

col1.metric("Articles", len(articles))
col2.metric("Sources", len(sources))
col3.metric("Category", category.title())
for article in articles:

    st.divider()

    col1, col2 = st.columns([1, 3])

    with col1:

        if article["urlToImage"]:
            st.image(
                article["urlToImage"],
                use_container_width=True
            )

    with col2:

        st.subheader(article["title"])

        published = article["publishedAt"]

        try:
            published = datetime.strptime(
                published,
                "%Y-%m-%dT%H:%M:%SZ"
            ).strftime("%d %b %Y %I:%M %p")
        except:
            pass

        st.caption(
            f"{article['source']['name']} • {published}"
        )

        st.write(
            article.get(
                "description",
                "No description available."
            )
        )

        st.link_button(
            "Read Full Article",
            article["url"]
        )
        
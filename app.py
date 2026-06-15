```python
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Advanced News Explorer",
    page_icon="📰",
    layout="wide"
)

# -----------------------------
# Constants
# -----------------------------
BASE_URL = "https://newsapi.org/v2/top-headlines"

countries = {
    "India": "in",
    "United States": "us",
    "United Kingdom": "gb",
    "Australia": "au",
    "Canada": "ca",
    "Germany": "de",
    "France": "fr",
    "Japan": "jp",
    "Singapore": "sg",
    "New Zealand": "nz"
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

# -----------------------------
# Fetch News Function
# -----------------------------
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


# -----------------------------
# App Header
# -----------------------------
st.title("📰 Advanced News Explorer")

st.write(
    "Stay informed with the latest headlines from around the world."
)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("News Filters")

selected_country = st.sidebar.selectbox(
    "Select Country",
    list(countries.keys())
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)

keyword = st.sidebar.text_input(
    "Search by Keyword",
    placeholder="e.g. AI, Tesla, Cricket"
)

article_count = st.sidebar.slider(
    "Number of Articles",
    min_value=5,
    max_value=50,
    value=10
)

fetch_button = st.sidebar.button("Fetch News")

# -----------------------------
# Main Logic
# -----------------------------
if fetch_button:

    with st.spinner("Fetching latest news..."):

        try:
            data = fetch_news(
                countries[selected_country],
                selected_category,
                keyword,
                article_count
            )

            articles = data.get("articles", [])

        except requests.exceptions.HTTPError as e:
            st.error(f"HTTP Error: {e}")
            st.stop()

        except requests.exceptions.ConnectionError:
            st.error("Network error. Please check your internet connection.")
            st.stop()

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            st.stop()

    if len(articles) == 0:
        st.warning("No articles found.")

    else:
        st.success(f"Found {len(articles)} articles.")

        # Dashboard Statistics
        sources = {}

        for article in articles:
            source = article.get("source", {}).get("name", "Unknown")
            sources[source] = sources.get(source, 0) + 1

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Articles", len(articles))

        with col2:
            st.metric("Sources", len(sources))

        with col3:
            st.metric("Category", selected_category.title())

        st.divider()

        # Source Breakdown Table
        with st.expander("📊 Source Breakdown"):

            df = pd.DataFrame({
                "Source": list(sources.keys()),
                "Articles": list(sources.values())
            })

            st.dataframe(
                df.sort_values(
                    by="Articles",
                    ascending=False
                ),
                use_container_width=True
            )

        # Display Articles
        for index, article in enumerate(articles, start=1):

            st.divider()

            col1, col2 = st.columns([1, 3])

            with col1:
                image_url = article.get("urlToImage")

                if image_url:
                    st.image(
                        image_url,
                        use_container_width=True
                    )

            with col2:
                st.subheader(
                    f"{index}. {article.get('title', 'No Title')}"
                )

                source = article.get(
                    "source",
                    {}
                ).get(
                    "name",
                    "Unknown Source"
                )

                published = article.get("publishedAt")

                if published:
                    try:
                        published = datetime.strptime(
                            published,
                            "%Y-%m-%dT%H:%M:%SZ"
                        ).strftime("%d %b %Y • %I:%M %p")
                    except ValueError:
                        pass

                st.caption(
                    f"📰 {source} | ⏰ {published}"
                )

                description = article.get(
                    "description",
                    "No description available."
                )

                st.write(description)

                author = article.get("author")

                if author:
                    st.write(f"**Author:** {author}")

                article_url = article.get("url")

                if article_url:
                    st.link_button(
                        "Read Full Article",
                        article_url
                    )

else:
    st.info(
        "Choose your filters from the sidebar and click "
        "'Fetch News' to view the latest headlines."
    )
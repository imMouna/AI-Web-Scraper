import streamlit as st
from scrape import scrape_website, clean_body_content, extract_body_content
from parse import parse_with_ollama

# Page Setup
st.set_page_config(page_title="AI Web Scraper", page_icon="🌐", layout="wide")

# Sidebar Navigation
with st.sidebar:
    st.title("AI Web Scraper")
    option = st.radio("Choose an action:", ["Scrape Website", "Parse Content"])

if option == "Scrape Website":
    st.header("🌐 Scrape a Website")
    url = st.text_input("Enter a Website URL:", placeholder="https://example.com")
    
    if st.button("Scrape"):
        if url.startswith("http"):
            st.info("Scraping the website...")
            try:
                raw_html = scrape_website(url)
                body_content = extract_body_content(raw_html)
                cleaned_content = clean_body_content(body_content)

                st.success("Website scraped successfully!")
                with st.expander("View Raw Content"):
                    st.text_area("Raw Content", raw_html, height=300)
                with st.expander("View Cleaned Content"):
                    st.text_area("Cleaned Content", cleaned_content, height=300)

                st.session_state.cleaned_content = cleaned_content
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a valid URL.")

if option == "Parse Content":
    st.header("🧠 Parse Scraped Content")
    if "cleaned_content" in st.session_state:
        parse_description = st.text_area(
            "What information would you like to extract?",
            placeholder="e.g., Extract all email addresses.",
        )
        if st.button("Parse"):
            st.info("Parsing content...")
            dom_chunks = [st.session_state.cleaned_content]
            result = parse_with_ollama(dom_chunks, parse_description)
            st.success("Parsing completed!")
            st.text_area("Parsed Output", result, height=300)
    else:
        st.warning("Please scrape a website first.")
    
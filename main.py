import streamlit as st
import validators
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama

# Streamlit UI
st.title("AI Web Scraper")
url = st.text_input("Enter Website URL")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if not url or not validators.url(url):
        st.error("Please enter a valid URL.")
    else:
        st.write("Scraping the website...")

        try:
            # Scrape the website
            dom_content = scrape_website(url)

            if not dom_content:
                st.warning("No content retrieved. The website might block scraping.")
            else:
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)

                # Store in Streamlit session state
                st.session_state.dom_content = cleaned_content

                # Display content in an expandable text box
                with st.expander("View DOM Content"):
                    st.text_area("DOM Content", cleaned_content, height=300)

        except Exception as e:
            st.error(f"Error scraping website: {e}")

# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state and st.session_state.dom_content:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            try:
                dom_chunks = split_dom_content(st.session_state.dom_content)
                parsed_result = parse_with_ollama(dom_chunks, parse_description)
                st.write(parsed_result)
            except Exception as e:
                st.error(f"Error parsing content: {e}")

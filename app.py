import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            st.error("Failed to fetch the URL. Please check the URL and try again.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup

def extract_tags(soup):
    tags = {tag.name for tag in soup.find_all()}
    return sorted(tags)

def extract_elements_by_tags(soup, tag_names):
    elements = []
    for tag_name in tag_names:
        elements.extend(soup.find_all(tag_name))
    return elements

def get_full_image_url(base_url, src):
    return urljoin(base_url, src)

def display_text_and_images(elements, base_url):
    for element in elements:
        if element.name == "img" and element.get("src"):
            img_url = get_full_image_url(base_url, element.get("src"))
            st.image(img_url, caption=img_url)
        elif element.text.strip():
            st.write(element.text.strip())

# Streamlit UI
st.title("Schema Markup Validator & Web Scraper")

# Input URL
url = st.text_input("Enter the URL to scrape:", "https://example.com")

if url:
    # Display webpage preview
    st.write("**Webpage Preview:**")
    st.components.v1.iframe(url, height=400)

    # Fetch and parse HTML
    html = fetch_html(url)
    if html:
        soup = parse_html(html)

        # Extract and display tags for selection
        tags = extract_tags(soup)
        selected_tags = st.multiselect("Select tags or classes:", tags)

        if selected_tags:
            elements = extract_elements_by_tags(soup, selected_tags)
            st.write(f"Found {len(elements)} elements with selected tags.")

            # Display text and images based on selected tags
            display_text_and_images(elements, url)

import streamlit as st
import requests
from bs4 import BeautifulSoup

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

def extract_elements_by_tag(soup, tag_name):
    elements = soup.find_all(tag_name)
    return elements

def display_text_and_images(elements):
    for element in elements:
        if element.name == "img" and element.get("src"):
            img_url = element.get("src")
            st.image(img_url, caption=img_url)
        elif element.text.strip():
            st.write(element.text.strip())

# Streamlit UI
st.title("Schema Markup Validator & Web Scraper")

url = st.text_input("Enter the URL to scrape:", "https://example.com")

if url:
    html = fetch_html(url)
    if html:
        soup = parse_html(html)

        tags = extract_tags(soup)
        selected_tag = st.selectbox("Select a tag or class:", tags)

        if selected_tag:
            elements = extract_elements_by_tag(soup, selected_tag)
            st.write(f"Found {len(elements)} elements with tag: {selected_tag}")

            display_text_and_images(elements)

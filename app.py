import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Fungsi untuk mengambil HTML dari URL
def fetch_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            st.error("Failed to fetch the URL. Please check the URL and try again.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Fungsi untuk mem-parsing HTML
def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup

# Fungsi untuk mengekstrak semua tag yang ada di halaman
def extract_tags(soup):
    tags = {tag.name for tag in soup.find_all()}
    return sorted(tags)

# Fungsi untuk menampilkan elemen berdasarkan tag yang dipilih
def extract_elements_by_tags(soup, tag_names):
    elements = []
    for tag_name in tag_names:
        elements.extend(soup.find_all(tag_name))
    return elements

# Menggabungkan URL dasar dengan src gambar
def get_full_image_url(base_url, src):
    return urljoin(base_url, src)

# Fungsi untuk menampilkan teks dan gambar
def display_text_and_images(elements, base_url):
    for element in elements:
        if element.name == "img" and element.get("src"):
            img_url = get_full_image_url(base_url, element.get("src"))
            st.image(img_url, caption=img_url)
        elif element.text.strip():
            st.write(element.text.strip())

# Fungsi untuk menambahkan highlight ke elemen yang dipilih
def highlight_elements(soup, tag_names):
    for tag in soup.find_all(tag_names):
        tag['style'] = "border: 2px solid red; background-color: #ffeb3b;"  # Tambah highlight dengan warna kuning
    return str(soup)

# Streamlit UI
st.title("Schema Markup Validator & Web Scraper with Highlight")

# Input URL
url = st.text_input("Enter the URL to scrape:", "https://example.com")

if url:
    # Fetch and parse HTML
    html = fetch_html(url)
    if html:
        soup = parse_html(html)

        # Extract and display tags for selection
        tags = extract_tags(soup)
        selected_tags = st.multiselect("Select tags to highlight:", tags)

        if selected_tags:
            # Highlight the selected elements
            highlighted_html = highlight_elements(soup, selected_tags)

            # Display highlighted HTML
            st.write("**Webpage Preview with Highlighted Elements:**")
            st.components.v1.html(highlighted_html, height=600, scrolling=True)

            # Display extracted elements' content
            st.write("**Content of Selected Tags:**")
            elements = extract_elements_by_tags(soup, selected_tags)
            st.write(f"Found {len(elements)} elements with selected tags.")
            display_text_and_images(elements, url)

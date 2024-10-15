import streamlit as st
from bs4 import BeautifulSoup
import requests

# Fungsi untuk mengambil HTML dari URL
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Memastikan tidak ada error dalam permintaan
        return response.text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL: {e}")
        return None

# Fungsi untuk menampilkan tag HTML yang ditemukan berdasarkan beberapa tag atau class tertentu
def find_tags(html, tags=None, classes=None):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Mengubah input string menjadi list jika ada
    tags_list = [tag.strip() for tag in tags.split(",")] if tags else []
    classes_list = [cls.strip() for cls in classes.split(",")] if classes else []

    found_elements = []

    # Temukan elemen berdasarkan kombinasi tag dan kelas
    for tag in tags_list:
        for cls in classes_list:
            found_elements.extend(soup.find_all(tag, class_=cls))
    
    # Jika hanya ada tag, cari berdasarkan tag
    if not classes_list and tags_list:
        for tag in tags_list:
            found_elements.extend(soup.find_all(tag))
    
    # Jika hanya ada kelas, cari berdasarkan kelas
    if not tags_list and classes_list:
        for cls in classes_list:
            found_elements.extend(soup.find_all(class_=cls))

    # Hapus duplikasi jika ada
    return list(set(found_elements))

# UI Streamlit
st.title("Schema Markup Validator & HTML Tag Extractor")

# Input URL
url = st.text_input("Enter the URL to fetch:", "")

if url:
    html_content = fetch_html(url)
    if html_content:
        st.subheader("HTML Structure Options")
        
        # Pilihan untuk memilih beberapa tag tertentu
        st.write("Choose specific tags or classes to extract (separate multiple tags or classes with commas):")
        
        # Input untuk tag dan class yang ingin dicari
        tags = st.text_input("Enter the tag names (e.g., div, h1, p):", "")
        classes = st.text_input("Enter the class names (e.g., entry-title, entry-content):", "")
        
        if st.button("Extract Elements"):
            elements = find_tags(html_content, tags, classes)
            
            if elements:
                st.write(f"Found {len(elements)} elements:")
                for i, element in enumerate(elements):
                    st.markdown(f"**Element {i+1}:**")
                    st.code(element.prettify())
            else:
                st.write("No elements found matching the criteria.")

# Pilihan untuk menampilkan schema markup jika ada
st.subheader("Check for Schema Markup")
if html_content:
    soup = BeautifulSoup(html_content, 'html.parser')
    schema_markup = soup.find_all(type="application/ld+json")
    
    if schema_markup:
        for i, script in enumerate(schema_markup):
            st.markdown(f"**Schema Markup {i+1}:**")
            st.code(script.string)
    else:
        st.write("No schema markup found.")

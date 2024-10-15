import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os

def scrape_novel(url):
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Error fetching the URL")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Menampilkan semua elemen HTML untuk pemilihan
    all_elements = soup.find_all(True)  # Ambil semua tag HTML
    return soup, all_elements

def extract_selected_elements(soup, selected_tags):
    extracted_text = {}
    image_urls = []
    
    for tag in selected_tags:
        elements = soup.find_all(tag)
        extracted_text[tag] = "\n\n".join([element.get_text() for element in elements])
        # Menyimpan URL gambar dari tag <img> dalam elemen yang dipilih
        if tag == 'img':
            image_urls.extend([img['src'] for img in elements if 'src' in img.attrs])
    
    return extracted_text, image_urls

def save_images(image_urls):
    saved_image_paths = []
    for i, url in enumerate(image_urls):
        img_response = requests.get(url)
        if img_response.status_code == 200:
            img = Image.open(BytesIO(img_response.content))
            image_path = f"image_{i + 1}.png"
            img.save(image_path)
            saved_image_paths.append(image_path)
    return saved_image_paths

st.title("Novel Scraper")

url = st.text_input("Masukkan URL novel:")

if st.button("Ambil Elemen"):
    if url:
        soup, all_elements = scrape_novel(url)
        if soup:
            # Menampilkan pilihan tag HTML
            st.header("Pilih Elemen untuk Di-scrape:")
            selected_tags = st.multiselect("Pilih tag HTML:", [element.name for element in all_elements])

            if st.button("Scrape Selected Elements"):
                if selected_tags:
                    extracted_content, image_urls = extract_selected_elements(soup, selected_tags)

                    # Menyimpan dan menampilkan konten yang diekstrak
                    for tag, content in extracted_content.items():
                        st.subheader(tag)
                        st.text_area(f"Konten dari <{tag}>", content, height=150)

                    # Mengunduh dan menampilkan gambar
                    if image_urls:
                        saved_images = save_images(image_urls)
                        st.header("Gambar:")
                        for img_path in saved_images:
                            st.image(img_path, caption=os.path.basename(img_path))
                else:
                    st.error("Silakan pilih tag untuk di-scrape.")
        else:
            st.error("Tidak ada konten yang ditemukan.")
    else:
        st.error("URL tidak boleh kosong.")

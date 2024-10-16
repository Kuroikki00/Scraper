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

    # Mengambil semua elemen HTML untuk pemilihan
    all_elements = soup.find_all(True)  # Ambil semua tag HTML
    return soup, all_elements

def extract_selected_elements(soup, selected_elements):
    extracted_content = {}
    image_urls = []

    for element in selected_elements:
        element_tag = element.name
        element_content = element.get_text(strip=True)

        # Menyimpan teks dan URL gambar dari tag <img>
        extracted_content[element_tag] = element_content
        if element_tag == 'img' and 'src' in element.attrs:
            image_urls.append(element['src'])

    return extracted_content, image_urls

def save_images(image_urls):
    saved_image_paths = []
    for i, url in enumerate(image_urls):
        img_response = requests.get(url)
        if img_response.status_code == 200:
            img = Image.open(BytesIO(img_response.content))
            # Menyimpan gambar dengan nama yang mencerminkan urutan
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
            # Menampilkan semua elemen untuk pemilihan
            st.header("Pilih Elemen untuk Di-scrape:")
            selected_elements = []
            for element in all_elements:
                if element.name not in ['script', 'style']:  # Menghindari elemen yang tidak relevan
                    content = element.get_text(strip=True)
                    st.checkbox(f"{element.name}: {content[:50]}...", key=element, value=False)  # Menampilkan 50 karakter pertama
                    selected_elements.append(element)

            if st.button("Scrape Selected Elements"):
                selected_keys = [element for element in selected_elements if st.checkbox(f"{element.name}: {element.get_text(strip=True)[:50]}...", value=False)]
                
                if selected_keys:
                    extracted_content, image_urls = extract_selected_elements(soup, selected_keys)

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
                    st.error("Silakan pilih elemen untuk di-scrape.")
        else:
            st.error("Tidak ada konten yang ditemukan.")
    else:
        st.error("URL tidak boleh kosong.")

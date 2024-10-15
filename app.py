import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Fungsi untuk melakukan scraping
def scrape_novel(url, title_selector, image_selector, text_selector):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Memeriksa apakah permintaan berhasil
        soup = BeautifulSoup(response.content, 'html.parser')

        # Mengambil elemen berdasarkan selector yang diberikan
        titles = soup.select(title_selector)
        images = soup.select(image_selector)
        texts = soup.select(text_selector)

        # Menyiapkan data untuk disimpan
        data = []
        for title, image, text in zip(titles, images, texts):
            data.append({
                'Title': title.get_text(strip=True),
                'Image URL': image['src'] if 'src' in image.attrs else None,
                'Text': text.get_text(strip=True)
            })

        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        st.error(f"Kesalahan saat mengakses URL: {e}")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong

# Streamlit UI
st.title("Novel Scraper")
url = st.text_input("Masukkan URL novel:")
title_selector = st.text_input("CSS Selector untuk Judul (contoh: h1.title):")
image_selector = st.text_input("CSS Selector untuk Gambar (contoh: img.cover):")
text_selector = st.text_input("CSS Selector untuk Teks (contoh: div.chapter):")

if st.button("Scrape"):
    if url and title_selector and image_selector and text_selector:
        df = scrape_novel(url, title_selector, image_selector, text_selector)
        if not df.empty:
            st.success("Scraping selesai!")
            st.dataframe(df)
            for index, row in df.iterrows():
                st.image(row['Image URL'], caption=row['Title'], use_column_width=True)
                st.write(row['Text'])
    else:
        st.error("Silakan isi semua field yang diperlukan.")

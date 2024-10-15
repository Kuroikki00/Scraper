import streamlit as st
from bs4 import BeautifulSoup
import requests
import streamlit.components.v1 as components

# Fungsi untuk menyorot elemen di web tampilan
def highlight_element(soup, element_id):
    script = f"""
    <script>
    function highlightElement() {{
        const el = document.querySelector('[data-id="{element_id}"]');
        if (el) {{
            el.style.backgroundColor = 'yellow';
            el.scrollIntoView({{behavior: 'smooth', block: 'center'}});
        }}
    }}
    highlightElement();
    </script>
    """
    return script

# Fungsi untuk membuat elemen HTML dengan data-id khusus untuk di-highlight
def add_data_id(soup):
    for idx, tag in enumerate(soup.find_all(True)):
        tag['data-id'] = idx
    return soup

# Fungsi untuk menampilkan HTML di streamlit
def render_html(html_content):
    components.html(html_content, height=600, scrolling=True)

# Layout utama
st.title("Web Scraping Developer Tools")
url = st.text_input("Masukkan URL halaman web yang ingin Anda scraping:")

if url:
    try:
        # Ambil konten HTML
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Tambahkan data-id ke setiap elemen untuk tracking
        soup = add_data_id(soup)

        # Tampilan kolom kiri dan kanan
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Website View")
            render_html(str(soup))

        with col2:
            st.subheader("HTML Elements")
            for idx, tag in enumerate(soup.find_all(True)):
                if st.button(f"{idx}: {tag.name}"):
                    # Ketika elemen diklik, buat script highlight
                    script = highlight_element(soup, idx)
                    render_html(str(soup) + script)

    except requests.exceptions.RequestException as e:
        st.error(f"Gagal memuat halaman: {e}")

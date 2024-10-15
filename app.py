import streamlit as st
from bs4 import BeautifulSoup
import requests
import streamlit.components.v1 as components

# Fungsi untuk menyorot elemen di tampilan web
def highlight_element(element_id):
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

# Fungsi untuk menambahkan data-id ke setiap elemen untuk tracking
def add_data_id(soup):
    for idx, tag in enumerate(soup.find_all(True)):
        tag['data-id'] = idx
    return soup

# Fungsi untuk menampilkan HTML di Streamlit
def render_html(html_content):
    components.html(html_content, height=600, scrolling=True)

# Fungsi untuk mendapatkan elemen berdasarkan class atau id
def get_elements_by_tag(soup, tags):
    elements = []
    for tag in soup.find_all(tags):
        identifier = tag.get('id') or tag.get('class')
        tag_repr = f"{tag.name}"
        if identifier:
            tag_repr += f" ({identifier})"
        elements.append((tag_repr, tag))
    return elements

# Fungsi untuk menampilkan elemen dengan hierarki
def display_element_tree(soup, parent_element=None, level=0):
    elements = soup.find_all(recursive=False) if parent_element is None else parent_element.find_all(recursive=False)
    for idx, element in enumerate(elements):
        identifier = element.get('id') or element.get('class')
        element_id = element.get('data-id')
        if identifier:
            name = f"{' ' * level * 2} - {element.name} ({identifier})"
        else:
            name = f"{' ' * level * 2} - {element.name}"
        
        if st.button(name):
            script = highlight_element(element_id)
            render_html(str(soup) + script)

        # Recursive call to display children
        display_element_tree(element, element, level + 1)

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
            st.subheader("HTML Element Hierarchy")
            display_element_tree(soup)

    except requests.exceptions.RequestException as e:
        st.error(f"Gagal memuat halaman: {e}")

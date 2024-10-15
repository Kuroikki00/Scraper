import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    """Fetch HTML content from the provided URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

def get_classes(html):
    """Extract all unique class names from the HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    classes = set()
    for tag in soup.find_all(True):  # Find all tags
        if 'class' in tag.attrs:
            classes.update(tag['class'])
    return list(classes)

def scrape_data(html, selected_classes):
    """Scrape data based on selected classes."""
    soup = BeautifulSoup(html, 'html.parser')
    data = {}
    for class_name in selected_classes:
        elements = soup.find_all(class_=class_name)
        paragraphs = []
        images = []
        
        for element in elements:
            # Get text from <p> tags
            for p in element.find_all('p'):
                paragraphs.append(p.get_text(strip=True))
            
            # Get images from <img> tags
            for img in element.find_all('img'):
                if 'src' in img.attrs:
                    images.append(img['src'])
        
        data[class_name] = {'paragraphs': paragraphs, 'images': images}
    return data

# Streamlit app
st.title("Novel Scraper")

url = st.text_input("Enter the URL of the novel page:")
if url:
    html_content = fetch_html(url)
    if html_content:
        classes = get_classes(html_content)
        selected_classes = st.multiselect("Select classes to scrape:", classes)

        if st.button("Scrape Data"):
            if selected_classes:
                scraped_data = scrape_data(html_content, selected_classes)
                st.success("Data Scraped Successfully!")

                # Displaying the scraped data
                for class_name, contents in scraped_data.items():
                    st.subheader(class_name)
                    
                    # Display paragraphs
                    if contents['paragraphs']:
                        for paragraph in contents['paragraphs']:
                            st.write(paragraph)
                    
                    # Display images
                    if contents['images']:
                        for img in contents['images']:
                            st.image(img, use_column_width=True)  # Display images with responsive width
            else:
                st.warning("Please select at least one class to scrape.")

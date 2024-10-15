import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_classes_from_url(url):
    """Get all unique class names from the specified URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    classes = set()
    for class_ in soup.find_all(class_=True):
        classes.update(class_.get('class'))
    
    return sorted(classes)

def scrape_novel_data(url, class_names):
    """Scrape text and images from a given URL based on the selected class names."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    extracted_text = []
    images = []
    
    for class_name in class_names:
        content = soup.find_all(class_=class_name)
        
        for item in content:
            # Collect text
            extracted_text.append(item.get_text(strip=True))
            
            # Collect images
            for img in item.find_all('img'):
                images.append(img['src'])
    
    return extracted_text, images

def main():
    st.title("Novel Scraper")
    
    st.sidebar.header("Input Options")
    
    # Input URL
    url = st.sidebar.text_input("Enter URL to Scrape:")
    
    if 'classes' not in st.session_state:
        st.session_state.classes = []
    
    if url:
        # Button to fetch classes
        if st.sidebar.button("Fetch Classes"):
            with st.spinner("Fetching classes..."):
                classes = get_classes_from_url(url)
                st.session_state.classes = classes  # Store classes in session state
                
            if classes:
                st.sidebar.header("Available Classes")
                # Allow multiple selections
                selected_classes = st.sidebar.multiselect("Select Classes to Scrape:", st.session_state.classes)
                st.session_state.selected_classes = selected_classes  # Store selected classes in session state
            else:
                st.error("No classes found at the provided URL.")
        else:
            selected_classes = st.session_state.get('selected_classes', [])
    else:
        selected_classes = st.session_state.get('selected_classes', [])

    # Check if classes are selected
    if selected_classes:
        # Unique Scrape button
        if st.sidebar.button("Scrape Now"):
            with st.spinner("Scraping..."):
                text_data, image_data = scrape_novel_data(url, selected_classes)
                
            # Displaying the results
            st.header("Scraped Data")
            st.subheader("Text Content:")
            for text in text_data:
                st.write(text)
                
            st.subheader("Images:")
            for img_url in image_data:
                st.image(img_url)
    elif st.sidebar.button("Scrape Now"):
        st.error("Please select at least one class to scrape.")

if __name__ == "__main__":
    main()

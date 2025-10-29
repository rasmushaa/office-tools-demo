import streamlit as st


def init_sidebar():
    with st.sidebar:
        st.sidebar.title("Office Tools Demo")
        st.page_link('frontend/home/home_page.py', label="Home", icon=":material/home:")

        st.divider()

        uploaded_file = st.file_uploader('Upload an Excel file', type=['xls', 'xlsx'])
    
        if not uploaded_file:
            st.info('Select a file for analysis')
            st.stop()
        else:
            return uploaded_file
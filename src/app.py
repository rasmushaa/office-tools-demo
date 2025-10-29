import streamlit as st
import backend

if 'backend' not in st.session_state:
    st.session_state['backend'] = backend

# Navigation Setup
all_pages = [
    st.Page('frontend/home/home_page.py', default=True),
    st.Page('frontend/email/template_loader_page.py'),
    st.Page('frontend/email/template_uploader_page.py'),
    st.Page('frontend/excel/excel_page.py'),
]

pg = st.navigation(
    all_pages,
    position='hidden'
)

# Main Event Run
pg.run() 
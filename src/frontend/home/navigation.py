import streamlit as st


def init_sidebar():
    with st.sidebar:
        st.sidebar.title("Office Tools Demo")
        st.page_link('frontend/email/template_loader_page.py', label="Email Templates", icon=":material/email:")
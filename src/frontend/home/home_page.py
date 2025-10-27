import streamlit as st
from frontend.home.navigation import init_sidebar


st.set_page_config(
    page_title="Office Tools Demo",
    layout="centered",
)

init_sidebar()

st.title("Welcome to Office Tools Demo!")
st.write("This is a demo application showcasing various office tools built with Streamlit.")
st.write("Use the sidebar to navigate between different tools.")
st.balloons()
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

st.divider()

st.subheader(':orange[Get your mock files to test the tools]')
with open('src/assets/mock/office-excel.xls', "rb") as file:
    if st.download_button(
        label="Download Excel",
        data=file,
        file_name='office-excel.xls',
    ):
        st.balloons()
with open('src/assets/mock/office-template.yaml', "rb") as file:
    if st.download_button(
        label="Download Email template",
        data=file,
        file_name='office-template.yaml',
    ):
        st.toast("Lets Go!", icon='😎')

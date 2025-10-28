import streamlit as st
from frontend.email.navigation import init_sidebar

st.set_page_config(
    page_title="Email Templates",
    layout="wide",
)

init_sidebar()


if not st.session_state['email']['active_template'] :
    st.title('Choose an Email template from the sidebar')
    st.stop()


col1, _, col2 = st.columns([5, 1, 10])

with col1:
    st.session_state['email']['active_template'] .render()
    checkbox = st.checkbox("Show Source File", value=False)

with col2:
    st.header("Generated Email Content")
    st.write("Copy the generated email content from right corner.")
    st.code(st.session_state['email']['active_template'] .get_filled_template(), language='markdown')

    if checkbox:
        content = st.session_state['email']['active_template'] .get_source_file()
        st.text_area("Template Source", content, height='content', disabled=True)


import streamlit as st  
from frontend.common.log import Log

def __init_group_st():
    if 'email' not in st.session_state:
        st.session_state['email'] = {}
        st.session_state['email']['template'] = None
        st.session_state['email']['log'] = Log()


def init_sidebar():
    __init_group_st()
    with st.sidebar:
        st.title("Email Pages")
        st.page_link('frontend/home/home_page.py', label="Home", icon=":material/home:")
        st.page_link('frontend/email/template_uploader_page.py', label="Template Uploader", icon=":material/cloud_upload:")

        st.title("Email Templates")
        for key, template in st.session_state.backend.email.filesystem.scan_templates().items():

            if template['validity'] == st.session_state.backend.email.filesystem.validity_levels.INVALID:
                val = st.button(
                    label=f"{key}.yaml (Invalid)",
                    key=key,
                    disabled=True,
                    help=f"Error: {template['error']}",
                    icon='❌'
                )

            elif template['validity'] == st.session_state.backend.email.filesystem.validity_levels.WARNING:
                val = st.button(
                    label=f"{template['name']} (v{template['version']})",
                    key=key,
                    icon="⚠️",
                    help=f"Warning: {template['error']}",
                )
            else:
                val = st.button(
                    label=f"{template['name']} (v{template['version']})",
                    key=key,
                    help=template['description'],
                )
            if val:
                st.session_state['email']['template'] = template['path']
                st.switch_page('frontend/email/template_loader_page.py')
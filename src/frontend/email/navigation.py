import streamlit as st  
from frontend.common.log import Log

def __init_group_st():
    if 'email' not in st.session_state:
        st.session_state['email'] = {}
        st.session_state['email']['log'] = Log()
        st.session_state['email']['active_template'] = None
        # All Template object are loaded to dict only once, and the states remain during runtime
        st.session_state['email']['templates'] = st.session_state.backend.email.filesystem.get_template_objects()


def init_sidebar():
    __init_group_st()
    with st.sidebar:
        st.title("Email Pages")
        st.page_link('frontend/home/home_page.py', label="Home", icon=":material/home:")
        st.page_link('frontend/email/template_uploader_page.py', label="Template Uploader", icon=":material/cloud_upload:")

        # Dynamically load buttons for every template in st dict
        st.title("Email Templates")
        for key, template in st.session_state['email']['templates'].items():
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
                    label=f"{template['object'].name} (v{template['object'].version})",
                    key=key,
                    icon="⚠️",
                    help=f"Warning: {template['error']}",
                )
            else:
                val = st.button(
                    label=f"{template['object'].name} (v{template['object'].version})",
                    key=key,
                )

            # Button triggers the active template switching
            if val:
                templates = st.session_state['email']['templates']
                active_template = templates[key]
                template_object = active_template['object']
                template_object.update_defaults() # Render the template with previous values active
                st.session_state['email']['active_template'] = template_object
                st.switch_page('frontend/email/template_loader_page.py')
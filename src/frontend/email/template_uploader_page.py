import streamlit as st
import yaml
from frontend.email.navigation import init_sidebar
from pathlib import Path
from datetime import datetime
import os

st.set_page_config(
    page_title="Template Upload",
    layout="centered",
)

init_sidebar()


st.title('Uploade a new Email template for runtime.')

with st.form("Template file form", clear_on_submit=True):
    uploaded_files = st.file_uploader(
        'Select your local template .yaml files',
        accept_multiple_files=True,
        type=['yaml', 'yml']
    )
    submitted = st.form_submit_button('Upload')

    # destination: <repo>/src/assets/templates
    TEMPLATES_DIR = Path(__file__).resolve().parents[2] / "assets" / "templates"
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

    # Display logs from previous run
    while st.session_state['email']['log'].has_logs:
        st.session_state['email']['log'].render()

    if not submitted:
        st.stop()

    if not uploaded_files:
        st.info("No files selected.")
        st.stop()

    # Ensure we have a list
    if not isinstance(uploaded_files, (list, tuple)):
        uploaded_files = [uploaded_files]

    for uploaded_file in uploaded_files:

        try:
            # read bytes and decode to text for yaml
            content_bytes = uploaded_file.getvalue()
            content_text = content_bytes.decode("utf-8")
            data = yaml.safe_load(content_text)

            check = st.session_state.backend.email.filesystem.is_valid_template_yaml_object(data)
            levels = st.session_state.backend.email.filesystem.validity_levels

            # If invalid, skip
            if check['validity'] == levels.INVALID:
                st.session_state['email']['log'].append(f'Error: {uploaded_file.name} is not a valid template due to: {check["error"]}', st.session_state['email']['log'].level.ERROR)
                continue
        
            # sanitize filename and avoid overwriting existing files
            safe_name = Path(uploaded_file.name).name or f"template-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.yaml"
            dest = TEMPLATES_DIR / safe_name
            if dest.exists():
                stem = dest.stem
                suffix = dest.suffix or ".yaml"
                timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
                dest = TEMPLATES_DIR / f"{stem}-{timestamp}{suffix}"

            dest.write_bytes(content_bytes)

            # Log success messags after all steps
            if check['validity'] == levels.WARNING:
                st.session_state['email']['log'].append(f'Warning: {uploaded_file.name} has: {check["error"]}, but was still added', st.session_state['email']['log'].level.WARNING)
            else:
                st.session_state['email']['log'].append(f'Info: Added {uploaded_file.name} to runtime templates', st.session_state['email']['log'].level.SUCCESS)

        except yaml.YAMLError as ye:
            st.session_state['email']['log'].append(f'YAML parse error in {uploaded_file.name}: {ye}', st.session_state['email']['log'].level.ERROR)
        except Exception as e:
            st.session_state['email']['log'].append(f'Error: was not able to process {uploaded_file.name}: {e}', st.session_state['email']['log'].level.ERROR)

    st.rerun()



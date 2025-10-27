import streamlit as st
import datetime

st.markdown("# Email Template Demo")


my_name = st.sidebar.text_input("Your Name", value=st.session_state.get('my_name', '<>'))
st.session_state['my_name'] = my_name
selections = st.sidebar.pills("Topics", ['Thing1', 'Thing2', 'Thing3'], selection_mode="multi", default=['Thing1', 'Thing2'])


text = f"""Hello,\n\nthanks for the meeting on {datetime.date.today()}!"""
text += "\n\nHere are the topics we discussed:\n"
for topic in selections:
    if topic == 'Thing1':
        text += "\n- Thing 1: This is the first thing we talked about."
    elif topic == 'Thing2':
        text += "\n- Thing 2: This is the second thing we talked about."
    elif topic == 'Thing3':
        text += "\n- Thing 3: This is the third thing we talked about."
text += f"\n\nBest regards,\n{st.session_state['my_name']}"


with st.expander("Email Editor"):
    text_edited = st.text_area("Edit the email template below:", value=text, height='content')


st.code(text_edited, language='markdown')
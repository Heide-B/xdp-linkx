import streamlit as st
import pandas as pd

st.set_page_config(initial_sidebar_state="collapsed")
data = pd.read_csv('chatbot.csv')
for index, row in data.iterrows():
    st.session_state[row['question_eng']] = row['response_eng']

st.header("Welcome to TalX: The chatbot for XDP Patients")
if 'init' not in st.session_state:
    with st.form('Discussion'):
        st.write(f"Chatbot: Welcome! Would you prefer to chat in English or Filipino?")
        user_rep = st.write('Your Input:')
        eng = st.checkbox('English')
        fil = st.checkbox('Filipino')
        sub = st.form_submit_button('Send')
        if sub == True and eng == True:
            st.session_state.init = "English"
        elif sub == True and fil == True:
            st.session_state.init = "Filipino"
elif st.session_state.init  == "English":
    st.write("Chatbot: It's good to have you here! I can answer your questions about XDP. Feel free to ask any of the questions below.")
    inputs = st.text_input('You: ')
    inputs = set(inputs.split(' '))
    set2 = set(s2.split(' '))
    if inputs in set('What is XDP'.split(" ")):
    #q1 = st.checkbox("What is XDP")
 #   if q1:
        st.write(f"Chatbot: {st.session_state['What is XDP']}")
    q2 = st.checkbox("How common is XDP")
    if q2:
        st.write(f"Chatbot: {st.session_state['How common is XDP']}")
    q3 = st.checkbox("What causes XDP")
    if q3:
        st.write(f"Chatbot: {st.session_state['What causes XDP']}")
    q4 = st.checkbox("What are the symptoms of XDPXDP")
    if q4:
        st.write(f"Chatbot: {st.session_state['What are the symptoms of XDP']}")

elif st.session_state.init != '':
    st.write(f"Chatbot: {st.session_state[user_q]}")


footer="""<style>
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p><a href="https://heide-b-xdp-linkx-xdp-q0f98p.streamlitapp.com/">Return Home</a>
<p>Developed with ❤ by</p>
<p><strong>LinkX: Log and Information Exchange</strong></p>
</div>
"""

st.markdown(footer,unsafe_allow_html=True)

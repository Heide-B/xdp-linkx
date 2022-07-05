import streamlit as st
import pandas as pd

st.set_page_config(initial_sidebar_state="collapsed")
data = pd.read_csv('chatbot.csv')
for index, row in data.iterrows():
    st.session_state[row['question_eng']] = row['response_eng']

st.header("Welcome to TalX: The XDP chatbot")
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
    st.caption('Here are some suggested questions:')
    st.caption('What is XDP')
    st.caption('How common is XDP')
    st.caption('What are the symptoms of XDP')
    inputs = st.text_input('You: ')
    if inputs.lower() == 'what is xdp':
        st.write(f"Chatbot: {st.session_state['What is XDP']}")
    elif 'common' in inputs:
        st.write(f"Chatbot: {st.session_state['How common is XDP']}")
    elif inputs == "What causes XDP":
        st.write(f"Chatbot: {st.session_state['What causes XDP']}")
    elif 'symptoms' in inputs:
        st.write(f"Chatbot: {st.session_state['What are the symptoms of XDP']}")
    else:
        st.write("Chatbot: I'm sorry, I can't quite understand your question.")

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

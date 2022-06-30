import streamlit as st
import pandas as pd
import numpy as np
import os
import webbrowser
import time
import base64


st.set_page_config(initial_sidebar_state="collapsed")
session = list(st.server.server.Server.get_current()._session_info_by_id.keys())[0]
url = dict(st.server.server.Server.get_current()._get_session_info(session).ws.request.headers)
relative_url =url['Host']

def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
 
    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "png"
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

set_bg_hack('background.png')

st.image('logo1.jpg', width=200)
with st.empty():
    for seconds in range(1):
        st.title("Welcome to LinkX")
        time.sleep(3)
        st.title("Bringing you inclusive log and information exchange")
        time.sleep(2)
    st.write("")
        

c1,c2,c3 = st.columns([1,2,1])
style = """
.button {
  border: none;
  color: black;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: block;
  font-size: 16px;
  margin: auto;
  cursor: pointer;
}
"""

c2.markdown(f"""<style>{style}</style>
<a target="_self" href="https://heide-b-xdp-linkx-xdp-q0f98p.streamlitapp.com/Chatbot_for_XDP_Patients">
    <button class="button button1">
        💬 Chatbot for XDP Patients
    </button>
</a>""",unsafe_allow_html=True)

c2.title("")

c2.markdown(f"""<style>{style}</style>
<a target="_self" href="https://heide-b-xdp-linkx-xdp-q0f98p.streamlitapp.com/Submit_Monitoring_Sheets">
    <button class="button button1">
        📝 Record Symptoms
    </button>
</a>""",unsafe_allow_html=True)

c2.title("")

c2.write(f"""<style>{style}</style>
<a target="_self" href="https://heide-b-xdp-linkx-xdp-q0f98p.streamlitapp.com/Read_Up_On_XDP">
    <button class="button button1">
        📖 Read up on XDP
    </button>
</a>""", unsafe_allow_html=True)

c2.title("")

c2.write(f"""<style>{style}</style>
<a target="_self" href="https://heide-b-xdp-linkx-xdp-q0f98p.streamlitapp.com/Experts_Dashboard">
    <button class="button button1">
        🏢 Expert's Portal
    </button>
</a>""", unsafe_allow_html=True)

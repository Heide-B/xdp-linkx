import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import base64

ucred = ['admin']
upw = ['admin']
st.set_page_config(initial_sidebar_state="collapsed")

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

if 'login' not in st.session_state:
    st.session_state['login'] = False
data = pd.read_csv('patient_results.csv')
pts = pd.read_csv('patient_data.csv')

def patient_res():
    for patient in data['Patient ID'].unique():
        with st.expander(str(patient)):
            ex = pts[pts['Patient ID']==patient]
            p1 = data[data['Patient ID']==patient].drop(columns='Patient ID')
            h1, h2, h3 = st.columns([2,2,1])
            h1.header(patient)
            h2.subheader(ex['Hospital'].values[0])
            h3.download_button(label="Download patient data", data=p1.to_csv().encode('utf-8'), file_name=f'{patient}-clinical-data.csv',mime='text/csv')
            c1, c2, c3 = st.columns(3)
            c1.metric('Age',ex['Age'].values[0])
            c2.metric('Sex',ex['Gender'].values[0])
            c3.metric('Medication',ex['On medication'].values[0])
            cols = p1.columns.to_list()
            cols.remove('Date')
            fig = plt.figure(figsize=(10, 4))
            for i in cols:
                sns.lineplot(x='Date',y=i,data=p1,legend=True, label=i)
                plt.xticks(rotation=45)
                plt.yticks(np.arange(0,8, step=1))
                plt.ylabel('Symptom Severity')
            st.pyplot(fig)


if st.session_state['login'] == False:
    st.title('Only authorized individuals may view this page. Kindly login if you wish to view this content')
    with st.form("Log in for XDP Experts"):
        u = st.text_input('Username')
        p = st.text_input('Password', type='password')
        submitted = st.form_submit_button("Submit")
        if submitted and (u in ucred and p in upw):
            st.session_state['login'] = True
        elif submitted and not (u in ucred and p in upw):
            st.markdown("**INVALID CREDENTIALS**")
            st.session_state['login'] = False
else:
    st.header("Welcome to the LinkX Expert's Dashboard")
    st.write('Patient data are shown below, click the expander to view patient details and current progress of symptoms. You may also download the data per patient')
    patient_res()


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

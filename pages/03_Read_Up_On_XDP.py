import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")


st.title("The Sunshine Care Foundation Inc")
st.components.v1.iframe(src='https://sunshinecarefoundation.org/understand-xdp/', height=800, scrolling=True)

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
<p><a href="/">Return Home</a>
<p>Developed with ❤ by</p>
<p><strong>LinkX: Log and Information Exchange</strong></p>
</div>
"""

st.markdown(footer,unsafe_allow_html=True)
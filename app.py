import streamlit as st
from PIL import Image


st.set_page_config(page_title="Narrative Viz", layout="wide")

st.title("Football Performance Analysis")
st.write(Image.open('images/football.jpg'))
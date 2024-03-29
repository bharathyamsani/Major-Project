import streamlit as st
import streamlit_option_menu as som
import home
import model
import contact
import time
import os
from PIL import Image

script_directory = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_directory, "../Images/favicon.png")
image=Image.open(image_path)

st.set_page_config(
    page_title="Audio Cloning Detection",
    page_icon=image
)

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Home"

def render_page(selected_page):
    with st.spinner("Loading..."):
        if selected_page == "Home":
            home.show()
        elif selected_page == "Model":
            model.show()
        elif selected_page == "Contact":
            contact.show()
        time.sleep(1)

def update_page(selected_page):
    st.session_state["selected_page"] = selected_page

options = ["Home", "Model", "Contact"]

selected_page = som.option_menu(
    key=st.session_state["selected_page"],
    menu_title=None,
    options=options,
    icons=["house-door-fill","book","envelope"],
    default_index=options.index(st.session_state["selected_page"]),
    orientation="horizontal",
    on_change=update_page
)
update_page(selected_page)
render_page(st.session_state.selected_page)
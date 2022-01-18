from pathlib import Path
from pages import pages

from streamlit_multipage import MultiPage
import streamlit as st


def start_page(st, **prev_vars):
    st.title("Simple Independent Example")


app = MultiPage()
app.st = st
app.start_button = "Let's go!"
app.navbar_name = "Navigation"
app.next_page_button = "Next Page"
app.previous_page_button = "Previous Page"
app.navbar_style = "SelectBox"

app.add_app("Initial Page", start_page, initial_page=True)

for app_name, app_function in pages.items():
    app.add_app(app_name, app_function)

app.run()

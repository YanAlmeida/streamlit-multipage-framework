from pathlib import Path

from streamlit_multipage import MultiPage, start_app

from pages import pages

import streamlit as st


def start_page():
	st.markdown(Path("README.md").read_text())


start_app()

app = MultiPage()
app.st = st
app.initial_page = start_page
app.start_button = "Let's go!"
app.navbar_name = "Navigation"
app.next_page_button = "Next Page"
app.previous_page_button = "Previous Page"

for app_name, app_function in pages.items():
    app.add_app(app_name, app_function)

app.run()

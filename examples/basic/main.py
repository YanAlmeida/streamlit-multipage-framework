from pathlib import Path

from streamlit_multipage import MultiPage, start_app

from pages import pages

import streamlit as st


def start_page(st):
    st.markdown(Path("README.md").read_text())


start_app()

app = MultiPage()
app.st = st

app.add_app("Initial Page", start_page, initial_page=True)

for app_name, app_function in pages.items():
    app.add_app(app_name, app_function)

app.run()

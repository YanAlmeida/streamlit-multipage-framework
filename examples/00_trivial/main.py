import streamlit as st
from streamlit_multipage import MultiPage


def my_page(st, **state):
    st.title("My Amazing App")
    name = st.text_input("Your Name: ")
    st.write(f"Hello {name}!")


app = MultiPage()
app.st = st

app.add_app("Hello World", my_page)

app.run()

import streamlit as st
from streamlit_multipage import MultiPage


def my_page(st, **state):
    st.title("My Amazing App")
    name_ = state["name"] if "name" in state else ""
    name = st.text_input("Your Name: ", value=name_)
    st.write(f"Hello {name}!")

    MultiPage.save({"name": name})


app = MultiPage()
app.st = st

app.add_app("Hello World", my_page)

app.run()

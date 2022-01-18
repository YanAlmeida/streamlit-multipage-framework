import streamlit as st
from streamlit_multipage import MultiPage


def input_page(st, **state):
    st.title("Body Mass Index")

    weight_ = state["weight"] if "weight" in state else 0.0
    weight = st.number_input("Your weight (Kg): ", value=weight_)

    height_ = state["height"] if "height" in state else 0.0
    height = st.number_input("Your height (m): ", value=height_)

    if height and weight:
        MultiPage.save({"weight": weight, "height": height})


def compute_page(st, **state):
    st.title("Body Mass Index")

    if "weight" not in state or "height" not in state:
        st.warning("Enter your data before computing. Go to the Input Page")
        return

    weight = state["weight"]
    height = state["height"]

    st.metric("BMI", round(weight / height ** 2, 2))


def landing_page(st):
    st.title("This is a Multi Page Application")
    st.write("Feel free to leave give a star in the Github Repo")


def footer(st):
    st.write("Developed by [ELC](https://elc.github.io)")


def header(st):
    st.write("This app is free to use")


def sidebar(st):
    st.button("Donate (Dummy)")


app = MultiPage()
app.st = st

app.start_button = "Go to the main page"
app.navbar_name = "Other Pages:"
app.next_page_button = "Next Chapter"
app.previous_page_button = "Previous Chapter"
app.reset_button = "Delete Cache"
app.navbar_style = "SelectBox"

app.header = header
app.footer = footer
app.navbar_extra = sidebar

app.hide_menu = True
app.hide_navigation = True

app.add_app("Landing", landing_page, initial_page=True)
app.add_app("Input Page", input_page)
app.add_app("BMI Result", compute_page)

app.run()

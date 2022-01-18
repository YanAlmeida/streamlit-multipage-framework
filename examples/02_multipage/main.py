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


app = MultiPage()
app.st = st

app.add_app("Input Page", input_page)
app.add_app("BMI Result", compute_page)

app.run()

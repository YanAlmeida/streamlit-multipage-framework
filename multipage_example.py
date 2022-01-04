import streamlit as st
from multipage import save, MultiPage, start_app, clear_cache
from pathlib import Path


def startpage():
	st.markdown(Path("README.md").read_text())


def app1(**prev_vars):
    variables = prev_vars.get("App1", {})

    if not (variables and "start_index" in variables):
        variables["start_index"] = 0

    start_index = variables["start_index"]

    st.button("Do nothing...")

    var1 = 10
    var2 = 5

    if st.button("Click here to save the variables..."):
        st.write("First number: " + str(var1))
        st.write("Second number: " + str(var2))
        save({"var1": var1, "var2": var2}, ["App2", "App3"])

    new_var_list = [
        "This framework rocks!",
        "This framework is really cool!",
        "I really liked this framework!",
    ]
    new_var = st.selectbox("Select an option: ", new_var_list, index=start_index)
    start_index = new_var_list.index(new_var)

    save({"start_index": start_index}, ["App1"])


def app2(**prev_vars):

    if not prev_vars:
        st.write("Ooops... You forgot to save the variables...")
        return

    variables = prev_vars.get("App2", {})
    required_variables = ["var1", "var2"]
    if any(variable not in variables for variable in required_variables):
        st.write("Missing one of the required variables")
        st.write(prev_vars)
        return

    var1 = variables["var1"]
    var2 = variables["var2"]

    if st.button("Click here to sum the variables"):
        sum_var = var1 + var2
        st.write(sum_var)

    if st.button("Click here to save a new variable"):
        var3 = 27
        st.write(var3)
        save({"var3": var3}, ["App3"])


def app3(**prev_vars):
    if not prev_vars:
        st.write("Ooops... You forgot to save the variables...")
        start_index = prev_vars
        save({"placeholder": start_index}, ["App1"])

        return

    variables = prev_vars.get("App3", {})
    required_variables = ["var1", "var2", "var3"]
    if any(variable not in variables for variable in required_variables):
        st.write("Missing one of the required variables")
        st.write(prev_vars)
        return

    var1 = variables["var1"]
    var2 = variables["var2"]
    var3 = variables["var3"]

    if st.button("Click here to erase the last variable"):
        clear_cache(["var3"], ["App3"])

    if st.button("Click here to multiply the variables"):
        st.write(var1 * var2 * var3)


start_app()

app = MultiPage()
app.initial_page = startpage
app.start_button = "Let's go!"
app.navbar_name = "Navigation"
app.next_page_button = "Next Page"
app.previous_page_button = "Previous Page"

app.add_app("App1", app1)
app.add_app("App2", app2)
app.add_app("App3", app3)
app.run()

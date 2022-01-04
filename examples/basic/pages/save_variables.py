from streamlit_multipage import save


def save_app(st, **prev_vars):
    variables = prev_vars.get("App1", {})

    if not (variables and "start_index" in variables):
        variables["start_index"] = 0

    start_index = variables["start_index"]

    st.button("Do nothing...")

    if st.button("Click here to save the variables..."):
        var1 = 10
        var2 = 5
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

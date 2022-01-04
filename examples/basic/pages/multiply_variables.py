from streamlit_multipage import save, clear_cache


def multiply_variables(st, **prev_vars):
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

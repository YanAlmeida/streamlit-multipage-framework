from streamlit_multipage import save


def sum_variables(st, **prev_vars):

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

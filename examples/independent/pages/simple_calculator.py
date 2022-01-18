import operator

from streamlit_multipage import save


def simple_calculator(st, **prev_vars):
    namespace = "SimpleCalculator"
    st.title("Simple Calculator")
    st.subheader(
        "A toy calculator that remember the numbers after you changed the page"
    )

    variables = prev_vars.get(namespace, {})
    required_variables = ["first", "second", "operation"]
    variable_present = [variable not in variables for variable in required_variables]

    if not all(variable_present) and any(variable_present):
        st.write("Some of the variables is missing")
        st.write(prev_vars)
        return
    elif not any(variable_present):
        first_ = variables["first"]
        second_ = variables["second"]
        operation_ = variables["operation"]
    else:
        first_ = 0
        second_ = 0
        operation_ = "Addition"

    first = st.number_input("First Value", value=first_)
    second = st.number_input("Second Value", value=second_)

    operations_supported = {
        "Addition": operator.add,
        "Multiplication": operator.mul,
    }

    operations = sorted(operations_supported.keys())
    index = operations.index(operation_)
    operation = st.selectbox("Operation", options=operations, index=index)

    function = operations_supported[operation]
    result = function(first, second)

    st.write(f"The Sum of the two number is: {result:.2f}")

    save({"first": first, "second": second, "operation": operation}, [namespace])

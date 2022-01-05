def compute_page(st, **state):
    st.title("Your Salary After Taxes")

    if "total" not in state:
        st.warning("Enter your data before computing. Go to the Input Page")
        return

    total = state["total"]

    st.metric("Total", round(total, 2))

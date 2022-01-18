import streamlit as st
from streamlit_multipage import MultiPage


def input_page(st, **state):
    namespace = "input"
    variables = state[namespace] if namespace in state else {}
    st.title("Tax Deduction")

    salary_ = variables["salary"] if "salary" in variables else 0.0
    salary = st.number_input("Your salary (USD): ", value=salary_)

    tax_percent_ = variables["tax_percent"] if "tax_percent" in variables else 0.0
    tax_percent = st.number_input("Taxes (%): ", value=tax_percent_)

    total = salary * (1 - tax_percent)

    if tax_percent and salary:
        MultiPage.save(
            {"salary": salary, "tax_percent": tax_percent}, namespaces=[namespace]
        )

    if total:
        MultiPage.save({"total": total}, namespaces=[namespace, "result"])


def compute_page(st, **state):
    namespace = "result"
    variables = state[namespace] if namespace in state else {}
    st.title("Your Salary After Taxes")

    if "total" not in variables:
        st.warning("Enter your data before computing. Go to the Input Page")
        return

    total = variables["total"]

    st.metric("Total", round(total, 2))


app = MultiPage()
app.st = st

app.add_app("Input Page", input_page)
app.add_app("Net Salary", compute_page)

app.run()

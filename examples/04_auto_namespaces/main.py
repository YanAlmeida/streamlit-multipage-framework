import streamlit as st
from streamlit_multipage import MultiPage


def input_page(st, **state):
    st.title("Tax Deduction")

    salary_ = state["salary"] if "salary" in state else 0.0
    salary = st.number_input("Your salary (USD): ", value=salary_)

    tax_percent_ = state["tax_percent"] if "tax_percent" in state else 0.0
    tax_percent = st.number_input("Taxes (%): ", value=tax_percent_)

    total = salary * (1 - tax_percent)

    if tax_percent and salary:
        MultiPage.save(
            {"salary": salary, "tax_percent": tax_percent}, namespaces=["Input Page"]
        )

    if total:
        MultiPage.save({"total": total}, namespaces=["Net Salary"])


def compute_page(st, **state):
    st.title("Your Salary After Taxes")

    if "total" not in state:
        st.warning("Enter your data before computing. Go to the Input Page")
        return

    total = state["total"]

    st.metric("Total", round(total, 2))


app = MultiPage()
app.st = st

app.add_app("Input Page", input_page)
app.add_app("Net Salary", compute_page)

app.run()

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

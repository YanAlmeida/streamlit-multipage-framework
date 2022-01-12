# Streamlit Multipage

<center>
    <a href="https://github.com/ELC/streamlit-multipage/actions/workflows/python-publish.yml">
        <img src="https://github.com/ELC/streamlit-multipage/actions/workflows/python-publish.yml/badge.svg">
    </a>
    <a href="https://pepy.tech/project/streamlit-multipage">
        <img src="https://pepy.tech/badge/streamlit-multipage">
    </a>
    <a href="https://pypi.org/project/streamlit-multipage/">
        <img src="https://img.shields.io/pypi/v/streamlit-multipage">
    </a>
</center>

Simple Python package to implement multiple pages using streamlit.

```
pip install streamlit-multipage
```

## Getting started

### Simple single-page app

Given one streamlit app in a Python file like this:

```python
import streamlit as st

st.title("My Amazing App")
name = st.text_input("Your Name: ")
st.write(f"Hello {name}!")
```

Wrap it into a function with a `st` parameter and arbitrary keyword arguments.

```python
import streamlit as st
from streamlit_multipage import MultiPage


def my_page(st, **state):
    st.title("My Amazing App")
    name = st.text_input("Your Name: ")
    st.write(f"Hello {name}!")


app = MultiPage()
app.st = st

app.add_app("Hello World", my_page)

app.run()
```

This example is trivial and will not give any additional value. The next
example will introduce state persistance.

### Saving State

If the state should be persisted between re-runs (pressing `R`) o application
runs (running `streamlit run`). The variables can be saved by calling the
`save` function and accessed conveniently via the `state` dictionary.

```python
import streamlit as st
from streamlit_multipage import MultiPage


def my_page(st, **state):
    st.title("My Amazing App")
    name_ = state["name"] if "name" in state else ""
    name = st.text_input("Your Name: ", value=name_)
    st.write(f"Hello {name}!")

    MultiPage.save({"name": name})


app = MultiPage()
app.st = st

app.add_app("Hello World", my_page)

app.run()
```

### Multiple pages

When dealing with multiple pages, the workflow is the same. If reading, always
sanitize the input and make sure the values are available and correct.

```python
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
```

### Using Namespaces

When handling multiple pages, it is possible to have variable name collisions,
by default all variables are saved in a common namespace called `global` but it
is also possible to defined custom namepsaces. One page can write to many
namespaces at once.

```python
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
        MultiPage.save({"salary": salary, "tax_percent": tax_percent}, namespaces=[namespace])

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
```

### Automatic Namespaces

If the namespace is set to the same App name (first parameter of `add_app`) the
state will be pre-filtered before sending it to the function.

```python
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
        MultiPage.save({"salary": salary, "tax_percent": tax_percent}, namespaces=["Input Page"])

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
```

### Directory Structure

When dealing with multiple, complex pages, it is not convenient to have them
all in a single .py file. This example shows how to lay out the directory
structure to have an organize project.

```
.
└── root/
    ├── pages/
    │   ├── __init__.py
    │   ├── input_data.py
    │   └── result.py
    └── main.py/
```

#### input_data.py

```python
from streamlit_multipage import MultiPage


def input_page(st, **state):
    st.title("Tax Deduction")

    salary_ = state["salary"] if "salary" in state else 0.0
    salary = st.number_input("Your salary (USD): ", value=salary_)

    tax_percent_ = state["tax_percent"] if "tax_percent" in state else 0.0
    tax_percent = st.number_input("Taxes (%): ", value=tax_percent_)

    total = salary * (1 - tax_percent)

    if tax_percent and salary:
        MultiPage.save({"salary": salary, "tax_percent": tax_percent}, namespaces=["Input Page"])

    if total:
        MultiPage.save({"total": total}, namespaces=["Net Salary"])
```

#### Result.py

```python
def compute_page(st, **state):
    st.title("Your Salary After Taxes")

    if "total" not in state:
        st.warning("Enter your data before computing. Go to the Input Page")
        return

    total = state["total"]

    st.metric("Total", round(total, 2))
```

#### \_\_init\_\_.py

```python
from .input_data import input_page
from .result import compute_page

pages = {
    "Input Page": input_page,
    "Net Salary": compute_page,
}
```

#### main.py

```python
from pages import pages

import streamlit as st
from streamlit_multipage import MultiPage


app = MultiPage()
app.st = st

for app_name, app_function in pages.items():
    app.add_app(app_name, app_function)

app.run()
```

### Landing Page

In is also possible to show a landing page that will be show only on start up
and then redirect to the main app. The landing page is merely informative and
has no access to the state.

```python
import streamlit as st
from streamlit_multipage import MultiPage, save


def input_page(st, **state):
    """See Example on Multipage"""


def compute_page(st, **state):
    """See Example on Multipage"""


def landing_page(st):
    st.title("This is a Multi Page Application")
    st.write("Feel free to leave give a star in the Github Repo")


app = MultiPage()
app.st = st

app.add_app("Landing", landing_page, initial_page=True)
app.add_app("Input Page", input_page)
app.add_app("BMI Result", compute_page)

app.run()
```

### Customization

There is additional functionality to customized the UI. In this example all the
default text is replaced with custom messages.

```python
import streamlit as st
from streamlit_multipage import MultiPage, save


def input_page(st, **state):
    """See Example on Multipage"""


def compute_page(st, **state):
    """See Example on Multipage"""


def landing_page(st):
    """See Example on Landing Page"""


def footer(st):
    st.write("Developed by [ELC](https://elc.github.io)")


def header(st):
    st.write("This app is free to use")


def sidebar(st):
    st.button("Donate (Dummy)")


app = MultiPage()
app.st = st

app.start_button = "Go to the main page"
app.navbar_name = "Other Pages:"
app.next_page_button = "Next Chapter"
app.previous_page_button = "Previous Chapter"
app.reset_button = "Delete Cache"
app.navbar_style = "SelectBox"

app.header = header
app.footer = footer
app.navbar_extra = sidebar

app.hide_menu = True
app.hide_navigation = True

app.add_app("Landing", landing_page, initial_page=True)
app.add_app("Input Page", input_page)
app.add_app("BMI Result", compute_page)

app.run()
```

## Installation

### No Install

This is a really simple script, if introducing new and small dependencies is
not desired, simply copy and paste the content of the `src` folder into your
project (one single file). Beware that this method does not include all the
advantages of using a dependency such as updates, dependency tracking and so
on.

### Via Pip

Install by running

```
pip install streamlit-multipage
```

The only dependency is `streamlit` which should be already installed. It will
be installed automatically if not present. Optionally, `joblib` can be
installed if the `pickle` module cannot handle the object in the saved state.

## Similar projects

Having multi page streamlit app is something many people try to achieve,
therefore, many libraries were developed to achieved this goal. Some of them
are listed below:

- [Hydralit](https://github.com/TangleSpace/hydralit)
- [streamlit-multiapps](https://github.com/upraneelnihar/streamlit-multiapps)
- [streamlit-pages](https://github.com/bvenkatesh-ai/streamlit_pages)

If this project does not fit your needs, please check these as well.

## Maintainers

This project is maintained by Yan Almeida and Ezequiel Leonardo Castaño

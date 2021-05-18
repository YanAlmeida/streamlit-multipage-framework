# streamlit-multipage-framework
Framework for implementing multipage structure in streamlit apps.
It was inspired by upraneelnihar's project: https://github.com/upraneelnihar/streamlit-multiapps.

Developed by: Yan Almeida.

# Required Libraries
1. Streamlit (`pip install streamlit`);
2. Joblib (`pip install joblib`);
3. OS (`pip install os`).

# Code Elements

## Functions and Classes
1. function `initialize()` -> Runs when the program starts and sets the initial page as 0;
2. function `save(var_list, name, page_names)` -> Saves a list of variables, associates it with a name and defines which pages will receive these variables;
3. function `load(name)` -> Loads a var_list previously saved;
4. function `clear_cache()` -> Clears the variables in cache;
5. class `app` -> Class to create pages (apps), defined by two attributes: name and func (app script defined as a function in the code);
6. class `MultiPage` -> Class to create the MultiPage structure, defined by the following attributes: apps (a list containing the pages (apps)), next_page_button and previous_page_button (in order to define the label of the buttons that switch between pages), navbar_name (to set the navigation bar header) and block_navbar (to keep your app without a navigation bar).

## MultiPage Class Methods
1. `add_app(self, name, func)` -> Creates an app and adds it to the `apps` attribute;
2. `disable_navbar(self)` -> Remover the sidebar options
3. `run(self)` -> Creates a sidebar with buttons to switch between pages and runs the apps depending on the chosen page. It also keeps the variables defined in previous pages, if the app function correctly applies "save".

# How to use it
1. Download "multipage.py" and put it in the same folder as your app;
2. Import the class `MultiPage` and the function `save` from multipage.py;
3. Create a `MultiPage` object;
4. Set the buttons' labels (next_page_button and previous_page_button attributes) and the navigation bar name (navbar_name attribute);
5. Define the different pages (apps) as functions (use the `save` method in the end of each function if you need the app to remember the variables). If you do save variables, they are going to be passed as argument to the target functions;
6. Use the `add_app` method to include each one of the functions;
7. Use the `run` method.

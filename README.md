# streamlit-multipage-framework
Framework for implementing multipage structure in streamlit apps.
It was inspired by upraneelnihar's project: https://github.com/upraneelnihar/streamlit-multiapps.

# Required Libraries
1 - Streamlit (pip install streamlit);
2 - Joblib (pip install joblib);
3 - OS (pip install os).

# Code Elements:

## Functions and Classes
1 - function initialize() -> runs when the program starts and sets the initial page as 0;
2 - function save(var_list, name) -> saves a list of variables and associates it to a name;
3 - function load(name) -> loads a var_list previously saved;
4 - class "app" -> class to create pages (apps), defined by three attributes: name, func (app script defined as a function in the code) and var_list (list of variables to "store")
5 - class "MultiPage" -> class to create the MultiPage structure, defined by three attributes: apps (a list containing the pages (apps)), next_page_button and previous_page_button(in order to define the label of the buttons that switch between pages).

## MultiPage Class Methods
1 - add_app(self, name, func) -> Creates an app and adds it to the "apps" attribute;
2 - run(self) -> Creates a sidebar with buttons to switch between pages and runs the apps depending on the chosen page. It also keeps the variables defined in a previous page, if the "app" function correctly applies "save".

# How to use it
1 - Download "multipage.py" and put it in the same folder as your app;
2 - Create a folder named "cache";
3 - Import the class MultiPage and the function save from multipage.py;
4 - Create a MultiPage object;
5 - Set the buttons' labels (next_page_button and previous_page_button attributes);
6 - Define the different pages (apps) as functions (use the "save" method in the end of each function if you need the app to remember the variables);
7 - Use the "add_app" method to include each one of the functions. IMPORTANT: If you use the "save" function, it's necessary to use the same name in the "add_app" method;
8 - Use the "run" method.

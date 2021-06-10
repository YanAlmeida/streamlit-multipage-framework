import streamlit as st
from multipage import save, MultiPage, start_app, clear_cache

start_app() #Clears the cache when the app is started

app = MultiPage()
app.start_button = "Let's go!"
app.navbar_name = "Navigation"
app.next_page_button = "Next Page"
app.previous_page_button = "Previous Page"


def startpage():
	st.markdown("""# streamlit-multipage-framework
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
4. function `clear_cache(name=None)` -> Clears the variables in cache. Receives a list of variables to erase, but if none is given, clears all of the variables;
5. function `start_app()` -> Clears all the variables in the cache when the app is started (but not after this);
6. function `change_page(pag)` -> Sets the current page number as `pag`;
7. function `read_page()` -> Returns current page number;
8. class `app` -> Class to create pages (apps), defined by two attributes: name and func (app script defined as a function in the code);
9. class `MultiPage` -> Class to create the MultiPage structure, defined by the following attributes: apps (a list containing the pages (apps)), initial_page (used to set a starting page for the app, if needed), initial_page_set (used to determine whether a starting page is set or not), next_page_button and previous_page_button (in order to define the label of the buttons that switch between pages), navbar_name (to set the navigation bar header) and block_navbar (to keep your app without a navigation bar).

## MultiPage Public Attributes
1. `next_page_button` -> Defines the label of the "Next Page" button. Default: "Next Page";
2. `previous_page_button` -> Defines the label of the "Previous Page" button. Default: "Previous Page";
3. `start_button` -> Defines the label of the starting page button that starts the application (it's only used if the app has a starting page). Default: "Let's go!"
4. `navbar_name` -> Defines the Navigation Bar's name. Default: "Navigation";

## MultiPage Class Methods
1. `add_app(self, name, func)` -> Creates an app and adds it to the `apps` attribute;
2. `set_initial_page(self, func)` -> Sets a starting page to the program;
3. `disable_navbar(self)` -> Removes the navigation bar;
4. `run(self)` -> Creates a sidebar with buttons to switch between pages and runs the apps depending on the chosen page. It also keeps the variables defined in previous pages, if the app function correctly applies "save".

# How to use it
1. Download "multipage.py" and put it in the same folder as your app;
2. Import the class `MultiPage` and the function `save` from multipage.py;
3. Create a `MultiPage` object;
4. Set the buttons' labels (next_page_button and previous_page_button attributes) and the navigation bar name (navbar_name attribute);
5. Define the different pages (apps) as functions (use the `save` method in the end of each function if you need the app to remember the variables). If you do save variables, they are going to be passed as argument to the target functions;
6. Use the `add_app` method to include each one of the functions;
7. If you have a starting page for your program, include it by using the `set_initial_page` method;
8. Use the `run` method.""")


def app1(prev_vars): #First page
	if prev_vars != None:

		start_index = prev_vars  #Defines the start index for a selectbox (defined below) as the option previously chosen by the user
	else:
		start_index = 1 #Defines the start index for a selectbox (defined below) as 1

	st.button("Do nothing...")
	var1 = 10
	var2 = 5
	if st.button("Click here to save the variables..."):
		st.write("First number: " + str(var1))
		st.write('Second number: ' + str(var2))
		save(var_list=[var1, var2], name="App1", page_names=["App2", "App3"]) #Saves the variables to be used on the second and third pages.
		######

	#Shows how to set placeholders based on a selection
	new_var_list = ["This framework rocks!", "This framework is really cool!", "I really liked this framework!"]
	new_var = st.selectbox("Select an option: ", new_var_list, index=start_index) #Creates a selectbox in order to show how to keep the option chosen by the user even after he leaves the page...
	start_index = new_var_list.index(new_var)

	save([start_index], "placeholder1", ["App2", "App3"]) #Saves the variable "start_index" to be used again on the first page

def app2(prev_vars): #Second page
	if type(prev_vars) is int: #Checks if the user saved the variables previously
		st.write("Ooops... You forgot to save the variables...")
		start_index = prev_vars
		save([start_index], "placeholder", ["App1"])

	else:
		start_index, var1, var2 = prev_vars #Reads the variables previously saved
		if st.button("Click here to sum the variables"):
			sum_var = var1+var2
			st.write(sum_var)
			
		if st.button("Click here to save a new variable"):
			var3 = 27
			st.write(var3)
			save(var_list=[var3], name="last_var", page_names=["App3"])
		save([start_index], "placeholder", ["App1"])



		#####

def app3(prev_vars): #Third page
	if type(prev_vars) is int: #Checks if the user saved the variables previously
		st.write("Ooops... You forgot to save the variables...")
		start_index = prev_vars
		save([start_index], "placeholder", ["App1"])
	else:
		try: #Checks if the user saved the last variable on the second page
			start_index, var1, var2, var3 = prev_vars
			if st.button("Click here to erase the last variable"):
				clear_cache(["last_var"]) #Erases the variables saved under the name "last_var"

			if st.button("Click here to multiply the variables"):
				st.write(var1*var2*var3)
			save([start_index], "placeholder", ["App1"])
		except:
			st.write("Ooops... You forgot to save the last variable...")
			start_index = prev_vars[0]
			save([start_index], "placeholder", ["App1"])

app.set_initial_page(startpage)
app.add_app("App1", app1) #Adds first page (app1) to the framework
app.add_app("App2", app2) #Adds second page (app2) to the framework
app.add_app("App3", app3) #Adds third page (app3) to the framework
app.run() #Runs the multipage app!

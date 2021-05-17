import streamlit as st
from multipage import save, MultiPage, clear_cache

app = MultiPage()
app.navbar_name = "Navigation"
app.next_page_button = "Next Page"
app.previous_page_button = "Previous Page"

def app1():
	clear_cache()
	st.button("Do nothing...")
	var1 = 10
	var2 = 5
	if st.button("Click here to save the variables..."):
		st.write("First number: " + str(var1))
		st.write('Second number: ' + str(var2))
		save([var1, var2],"app1")
		######

def app2(prev_vars):
	try:
		var1, var2 = prev_vars
		if st.button("Click here to sum the variables"):
			sum_var = var1+var2
			st.write(sum_var)

		save([var1, var2], "app2")
	except:
		st.write("You forgot to save the variables...")


		#####

def app3(prev_vars):
	try:
		var1, var2 = prev_vars
		if st.button("Multiply"):
			st.write(var1*var2)
	except:
		st.write("Oops... Something went wrong...")

app.add_app("App1", app1)
app.add_app("App2", app2)
app.add_app("App3", app3)
app.run()

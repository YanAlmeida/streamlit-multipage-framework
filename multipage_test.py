import streamlit as st
from multipage import save, MultiPage, clear_cache

app = MultiPage()
app.navbar_name = "Navigation"
app.next_page_button = "Next Page"
app.previous_page_button = "Previous Page"

def app1(prev_vars):
	clear_cache()
	st.button("Do nothing...")
	var1 = 10
	var2 = 5
	if st.button("Click here to save the variables..."):
		st.write("First number: " + str(var1))
		st.write('Second number: ' + str(var2))
		save(var_list=[var1, var2], name="App1", page_names=["App2", "App3"])
		######

def app2(prev_vars):
	if prev_vars == None:
		st.write("Ooops... You forgot to save the variables...")

	else:
		var1, var2 = prev_vars
		if st.button("Click here to sum the variables"):
			sum_var = var1+var2
			st.write(sum_var)
			
		if st.button("Click here to save a new variable"):
			var3 = 27
			st.write(var3)
			save(var_list=[var3], name="App2", page_names=["App3"])



		#####

def app3(prev_vars):
	if prev_vars == None:
		st.write("Ooops... You forgot to save the variables...")
	else:
		try:
			var1, var2, var3 = prev_vars
			if st.button("Click here to multiply the variables"):
				st.write(var1*var2*var3)
		except:
			("Ooops... You forgot to save the last variable...")

app.add_app("App1", app1)
app.add_app("App2", app2)
app.add_app("App3", app3)
app.run()

import streamlit as st
from multipage import save, MultiPage

app = MultiPage()
app.next_page_button = "Next Page"
app.previous_page_button = "Previous Page"

def app1():
	st.button("Do nothing...")
	if st.button("Check numbers"):
		var1 = 10
		var2 = 5
		st.write("First number: " + str(var1))
		st.write('Second number: ' + str(var2))
		save([var1, var2],"app1")
		######

def app2(prev_vars):
	var1, var2 = prev_vars
	if st.button("Sum"):
		sum_var = var1+var2
		st.write(sum_var)
		save([var1, var2], "app2")
		#####

def app3(prev_vars):
	var1, var2 = prev_vars
	if st.button("Multiply"):
		st.write(var1*var2)

app.add_app("app1", app1)
app.add_app("app2", app2)
app.add_app("app3", app3)
app.run()

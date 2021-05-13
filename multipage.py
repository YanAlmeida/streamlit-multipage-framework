import streamlit as st
import os
import joblib

path = os.getcwd()
cache = os.path.join(path, 'cache')

@st.cache(suppress_st_warning=True)
def initialize():
	try:
		with open(os.path.join(cache, 'cache.txt'), "w") as f:
		    f.write("0")
		    f.close()
	except FileNotFoundError:
		os.mkdir(cache)
		with open(os.path.join(cache, 'cache.txt'), "w") as f:
		    f.write("0")
		    f.close()

def save(var_list, name):
	joblib.dump(var_list, os.path.join(cache, name + '.pkl'))
	return os.path.join(cache, name + '.pkl')

def load(name):
	try:
		return joblib.load(os.path.join(cache, name + '.pkl'))
	except FileNotFoundError:
		return ''


class app:
	def __init__(self, name, func, var_list):
		self.name = name
		self.func = func
		self.var_list = var_list


class MultiPage:
	def __init__(self, next_page="Next Page", previous_page="Previous Page"):
		self.apps = []
		self.next_page_button = next_page
		self.previous_page_button = previous_page


	def add_app(self, name, func):
		new_app = app(name, func, load(name))
		self.apps.append(new_app)

	def run(self):
		initialize()

		with open(os.path.join(cache, 'cache.txt'), "r") as f:
		    pag = f.readline()
		    pag = int(pag)
		    f.close()

		side_1, side_2 = st.sidebar.beta_columns(2)

		with side_1:
			if st.button(self.previous_page_button):
				if pag > 0:
					pag -= 1 
				else:
					pag = 0

				with open(os.path.join(cache, 'cache.txt'), "w") as f:
					f.truncate()
					f.write(f"{pag}")
					f.close()


		with side_2:
			if st.button(self.next_page_button):
			    if pag < len(self.apps)-1:
			    	pag +=1
			    else:
			    	pag = len(self.apps)-1 
			    with open(os.path.join(cache, 'cache.txt'), "w") as f:
			        f.truncate()
			        f.write(f"{pag}")
			        f.close()

		if pag==0:
			self.apps[pag].func()
		else:
			self.apps[pag].func(self.apps[pag-1].var_list)
			



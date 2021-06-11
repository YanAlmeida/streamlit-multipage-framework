import streamlit as st
import os
import joblib

path = os.getcwd()
cache = os.path.join(path, 'cache')

def change_page(pag):
	with open(os.path.join(cache, 'cache.txt'), "w") as f:
		f.truncate()
		f.write(f"{pag}")
		f.close()

def read_page():
	with open(os.path.join(cache, 'cache.txt'), "r") as f:
		pag = f.readline()
		pag = int(pag)
		f.close()
	return pag

@st.cache(suppress_st_warning=True)
def initialize(initial_page_test=False):
	if initial_page_test:
		toWrite= -1
	else:
		toWrite= 0
	try:
		change_page(toWrite)
	except FileNotFoundError:
		os.mkdir(cache)
		change_page(toWrite)

def save(var_list, name, page_names):
	try:
		dic = joblib.load(os.path.join(cache, 'dic.pkl'))
	except FileNotFoundError:
		dic = {}

	for app in page_names:
		if app in list(dic.keys()):
			if name not in dic[app]:
				dic[app] += [name]
		else:
			dic[app] = [name]


	joblib.dump(var_list, os.path.join(cache, name + '.pkl'))
	joblib.dump(dic, os.path.join(cache, 'dic.pkl'))

	return os.path.join(cache, name + '.pkl')

def load(name):
	try:
		return joblib.load(os.path.join(cache, name + '.pkl'))
	except FileNotFoundError:
		return ''

def clear_cache(filenames=None):
	if filenames:
		for element in filenames:
			os.remove(os.path.join(cache, element + '.pkl'))
	else:
		filelist = [file for file in os.listdir(cache) if file.endswith(".pkl")]
		for file in filelist:
			os.remove(os.path.join(cache, file))

@st.cache(suppress_st_warning=True)
def start_app():
	try:
		clear_cache()
	except:
		pass

class app:
	def __init__(self, name, func):
		self.name = name
		self.func = func


class MultiPage:
	def __init__(self, next_page="Next Page", previous_page="Previous Page", navbar_name="Navigation", start_button="Let's go!"):
		self.__initial_page = None
		self.start_button = start_button
		self.__initial_page_set = False
		self.__apps = []
		self.navbar_name = navbar_name
		self.__block_navbar = False
		self.next_page_button = next_page
		self.previous_page_button = previous_page

	def disable_navbar(self):
		self.__block_navbar = True

	def set_initial_page(self, func):
		self.__initial_page = app("__INITIALPAGE__", func)
		self.__initial_page_set = True


	def add_app(self, name, func):
		new_app = app(name, func)
		self.__apps.append(new_app)

	def run(self):
		initialize(self.__initial_page_set)

		pag = read_page()

		container_1 = st.beta_container()

		if pag == -1:
			container_2 = st.beta_container()
			placeholder = st.empty()
			with container_2:
				if placeholder.button(self.start_button):
					pag = 0
					change_page(pag)
					placeholder.empty()
		with container_1:
			if pag==-1:
				self.__initial_page.func()

			else:
				side_1, side_2 = st.sidebar.beta_columns(2)

				with side_1:
					if st.button(self.previous_page_button):
						if pag > 0:
							pag -= 1 
						else:
							pag = 0

						change_page(pag)


				with side_2:
					if st.button(self.next_page_button):
						if pag < len(self.__apps)-1:
							pag +=1
						else:
							pag = len(self.__apps)-1 

						change_page(pag)



				st.sidebar.markdown(f"""<h1 style="text-align:center;">{self.navbar_name}</h1>""", unsafe_allow_html=True)
				st.sidebar.text('\n')


				for i in range(len(self.__apps)):
					if st.sidebar.button(self.__apps[i].name):
						pag = i
						change_page(pag)

				try:
					prev_vars = []
					dic = joblib.load(os.path.join(cache, 'dic.pkl'))
					for appname in dic[self.__apps[pag].name]:
						prev_vars += load(os.path.join(cache, appname))
					if len(prev_vars) == 1:
						prev_vars = prev_vars[0]
				except:
					prev_vars = None

				self.__apps[pag].func(prev_vars)

from dataclasses import dataclass, field
from typing import List, Callable

from .helper import change_page, initialize, read_page, load

import streamlit as st


@dataclass
class App:
    name: str
    func: Callable


@dataclass
class MultiPage:
    __initial_page: App = None
    __apps: List[App] = field(default_factory=list)

    start_button: str = "Let's go!"
    navbar_name: str = "Navigation"
    next_page_button: str = "Next Page"
    previous_page_button: str = "Previous Page"

    @property
    def initial_page(self) -> App:
        return self.__initial_page

    @initial_page.setter
    def initial_page(self, func: Callable) -> None:
        self.__initial_page = App("__INITIALPAGE__", func)

    @property
    def __initial_page_set(self) -> bool:
        return self.__initial_page is not None

    def add_app(self, name: str, func: Callable) -> None:
        new_app = App(name, func)
        self.__apps.append(new_app)

    def run(self) -> None:
        initial_page = -1 if self.__initial_page_set else 0
        initialize(initial_page)

        page = read_page()

        container_1 = st.container()

        if page == -1:
            container_2 = st.container()
            placeholder = st.empty()
            with container_2:
                if placeholder.button(self.start_button):
                    page = 0
                    change_page(page)
                    placeholder.empty()

        with container_1:
            if page == -1:
                self.__initial_page.func()
                return

            side_1, side_2 = st.sidebar.columns(2)

            with side_1:
                if st.button(self.previous_page_button):
                    page = max(0, page - 1)
                    change_page(page)

            with side_2:
                if st.button(self.next_page_button):
                    page = min(len(self.__apps) - 1, page + 1)
                    change_page(page)

            st.sidebar.markdown(
                f"""<h1 style="text-align:center;">{self.navbar_name}</h1>""",
                unsafe_allow_html=True,
            )
            st.sidebar.text("\n")

            for i in range(len(self.__apps)):
                if st.sidebar.button(self.__apps[i].name):
                    page = i
                    change_page(page)

            data = load()

            print(data)

            self.__apps[page].func(**data)

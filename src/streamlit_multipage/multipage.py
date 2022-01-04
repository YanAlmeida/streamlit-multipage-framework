from dataclasses import dataclass, field
from typing import List, Callable

from .helper import change_page, initialize, read_page, load


@dataclass
class App:
    name: str
    func: Callable


@dataclass
class MultiPage:
    st = None
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

        container_1 = self.st.container()

        if page == -1:
            container_2 = self.st.container()
            placeholder = self.st.empty()
            with container_2:
                if placeholder.button(self.start_button):
                    page = 0
                    change_page(page)
                    placeholder.empty()

        with container_1:
            if page == -1:
                self.__initial_page.func()
                return

            side_1, side_2 = self.st.sidebar.columns(2)

            with side_1:
                if self.st.button(self.previous_page_button):
                    page = max(0, page - 1)
                    change_page(page)

            with side_2:
                if self.st.button(self.next_page_button):
                    page = min(len(self.__apps) - 1, page + 1)
                    change_page(page)

            self.st.sidebar.markdown(
                f"""<h1 style="text-align:center;">{self.navbar_name}</h1>""",
                unsafe_allow_html=True,
            )
            self.st.sidebar.text("\n")

            for index, app in enumerate(self.__apps):
                if self.st.sidebar.button(app.name):
                    change_page(index)

            data = load()

            self.__apps[page].func(self.st, **data)

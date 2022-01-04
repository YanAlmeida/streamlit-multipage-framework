from dataclasses import dataclass, field
from typing import List, Callable, NamedTuple

from .helper import change_page, initialize, read_page, load


class App(NamedTuple):
    name: str
    func: Callable


@dataclass
class MultiPage:
    st = None
    __apps: List[App] = field(default_factory=list)
    __initial_page: App = None
    start_button: str = "Let's go!"
    navbar_name: str = "Navigation"
    next_page_button: str = "Next Page"
    previous_page_button: str = "Previous Page"
    navbar_style = "Button"


    def add_app(self, name: str, func: Callable, initial_page: bool = False) -> None:
        if initial_page:
            self.__initial_page = App("__INITIALPAGE__", func)
            initialize(-1)
            return

        new_app = App(name, func)
        self.__apps.append(new_app)


    def _render_navbar(self, sidebar) -> None:
        page = read_page()

        left_column, _, right_column = sidebar.columns(3)

        if left_column.button(self.previous_page_button):
            page = max(0, page - 1)
            change_page(page)

        if right_column.button(self.next_page_button):
            page = min(len(self.__apps) - 1, page + 1)
            change_page(page)

        sidebar.markdown(
            f"""<h1 style="text-align:center;">{self.navbar_name}</h1>""",
            unsafe_allow_html=True,
        )
        sidebar.text("\n")

        possible_styles = ["Button", "SelectBox"]

        if self.navbar_style not in possible_styles:
            sidebar.warning("Invalid Navbar Style - Using Button")
            self.navbar_style = "Button"

        if self.navbar_style == "Button":
            columns = sidebar.columns(len(self.__apps))
            for index, (columnm, app) in enumerate(zip(columns, self.__apps)):
                if columnm.button(app.name):
                    change_page(index)
        
        if self.navbar_style == "SelectBox":
            app_names = [app.name for app in self.__apps]
            app_name = sidebar.selectbox("", app_names)
            next_page = app_names.index(app_name)
            change_page(next_page)

        sidebar.write("---")


    def _render_landing_page(self, st):
        page = read_page()

        if page != -1:
            return False

        body = self.st.container()
        footer = self.st.container()

        if footer.button(self.start_button):
            change_page(0)

        self.__initial_page.func(body)
        initialize(0)

        return True


    def run(self) -> None:
        landing_page = self._render_landing_page(self.st)

        if landing_page:
            return

        self._render_navbar(self.st.sidebar)

        data = load()

        page = read_page()
        self.__apps[page].func(self.st, **data)

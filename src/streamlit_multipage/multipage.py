from dataclasses import dataclass, field
from typing import List, Callable, NamedTuple, ClassVar, Any, Dict, Union
from collections import defaultdict
from pathlib import Path

import streamlit as st

try:
    import joblib

    pickling = joblib
except ImportError:
    import pickle

    pickling = pickle


@dataclass
class StateManager:
    path: Path = Path(__file__).resolve().parent
    cache: Path = path / "cache"
    cache_filename: str = "data.pkl"

    @property
    def cache_file(self) -> Path:
        return self.cache / self.cache_filename

    def change_page(self, page: int) -> None:
        self.save({"current_page": page}, ["global"])

    def _read_page(self) -> int:
        data = self._load()["global"]

        if "current_page" in data:
            return int(data["current_page"])

        return -1

    @st.cache(suppress_st_warning=True)
    def _initialize(self, initial_page: int) -> None:
        self.change_page(initial_page)

    def save(self, variables: Dict[str, Any], namespaces: List[str] = None) -> None:
        if namespaces is None:
            namespaces = ["global"]

        if not variables:
            return

        data = self._load()

        new_data = {namespace: variables for namespace in namespaces}

        for namespace, variables in new_data.items():
            if namespace in data:
                data[namespace].update(variables)
                continue

            data[namespace] = variables

        self._save(data)

    def _save(self, data: Dict[str, Any]) -> None:
        self.cache.mkdir(parents=True, exist_ok=True)
        pickling.dump(data, self.cache_file)

    def _load(self) -> Dict[str, Any]:
        if not self.cache_file.exists():
            return defaultdict(dict)

        data = pickling.load(self.cache_file)
        if "global" in data:
            data.update(data["global"])

        return data

    def clear_cache(
        self,
        variables: Dict[str, Any] = None,
        namespaces: List[str] = None,
        all_variables: bool = False,
    ) -> None:

        if not variables or not namespaces:
            return

        if all_variables:
            self.cache_file.unlink(missing_ok=True)
            return

        data = self._load()
        for namespace in namespaces:
            for variable in variables:
                if variable not in data[namespace]:
                    continue

                del data[namespace][variable]

        self._save(data)


state = StateManager()


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
    reset_button: str = "Reset Cache"
    navbar_style = "Button"
    __state_manager: ClassVar[StateManager] = state

    def add_app(self, name: str, func: Callable, initial_page: bool = False) -> None:
        if initial_page:
            self.__initial_page = App("__INITIALPAGE__", func)
            return

        new_app = App(name, func)
        self.__apps.append(new_app)

    def _render_navbar(self, sidebar) -> None:
        page = self.__state_manager._read_page()

        left_column, middle_column, right_column = sidebar.columns(3)

        if middle_column.button(self.reset_button):
            self.clear_cache(True, True, True)
            self.change_page(-1)

        if left_column.button(self.previous_page_button):
            page = max(0, page - 1)
            self.__state_manager.change_page(page)

        if right_column.button(self.next_page_button):
            page = min(len(self.__apps) - 1, page + 1)
            self.__state_manager.change_page(page)

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
                    self.__state_manager.change_page(index)

        if self.navbar_style == "SelectBox":
            app_names = [app.name for app in self.__apps]
            app_name = sidebar.selectbox("", app_names)
            next_page = app_names.index(app_name)
            self.__state_manager.change_page(next_page)

        sidebar.write("---")

    def _render_landing_page(self) -> bool:
        page = self.__state_manager._read_page()

        if page != -1 or not self.__initial_page:
            return False

        body = self.st.container()
        footer = self.st.container()

        if footer.button(self.start_button):
            self.__state_manager.change_page(0)

        self.__initial_page.func(body)
        self.__state_manager.change_page(0)

        return True

    def _run(self) -> None:

        landing_page = self._render_landing_page()

        if landing_page:
            return

        self._render_navbar(self.st.sidebar)

        page = self.__state_manager._read_page()

        if page == -1:
            landing_page = self._render_landing_page()

            if landing_page:
                return

        data = self.__state_manager._load()

        if page >= len(self.__apps):
            page = -1

        app = self.__apps[page]

        if app.name in data:
            data = data[app.name]

        app.func(self.st, **data)

    def run(self, avoid_collisions: bool = True) -> None:
        if avoid_collisions:
            import hashlib

            app_names = sorted(app.name for app in self.__apps)
            names_concatenated = "".join(app_names).encode("utf-8")
            cache_filename = (
                hashlib.sha256(names_concatenated).hexdigest()[-10:] + ".pkl"
            )
            self.__state_manager.cache_filename = cache_filename

        self._run()

    @classmethod
    def clear_cache(
        cls,
        variables: Dict[str, Any] = None,
        namespaces: List[str] = None,
        all_variables: bool = False,
    ) -> None:
        cls.__state_manager.clear_cache(variables, namespaces, all_variables)

    @classmethod
    def save(cls, variables: Dict[str, Any], namespaces: List[str] = None) -> None:
        cls.__state_manager.save(variables, namespaces)

    @classmethod
    def change_page(cls, page: int) -> None:
        cls.__state_manager.change_page(page)

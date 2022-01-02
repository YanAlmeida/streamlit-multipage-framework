import json
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Callable, Any, Dict
from pathlib import Path

import streamlit as st
import joblib

path = Path(__file__).resolve().parent
cache = path / "cache"
cache_file = cache / "data.pkl"


def change_page(page: int) -> None:
    save({"current_page": page}, ["global"])


def read_page() -> int:
    data = load()["global"]

    if "current_page" in data:
        return int(data["current_page"])

    return 0


@st.cache(suppress_st_warning=True)
def initialize(initial_page: int) -> None:
    change_page(initial_page)


def save(variables: Dict[str, Any], namespaces: List[str]) -> None:
    if not variables or not namespaces:
        return

    data = load()

    new_data = {namespace: variables for namespace in namespaces}

    for namespace, variables in new_data.items():
        if namespace in data:
            data[namespace].update(variables)
            continue

        data[namespace] = variables

    _save(data)


def _save(data: Dict[str, Any]) -> None:
    cache.mkdir(parents=True, exist_ok=True)
    joblib.dump(data, cache_file)


def load() -> Dict[str, Any]:
    if not cache_file.exists():
        return defaultdict(dict)

    return joblib.load(cache_file)


def clear_cache(
    variables: Dict[str, Any] = None,
    namespaces: List[str] = None,
    all_variables: bool = False,
) -> None:
    if variables and namespaces:
        data = load()
        for namespace in namespaces:
            for variable in variables:
                print(variable, namespace)
                if variable not in data[namespace]:
                    continue

                del data[namespace][variable]

        _save(data)

    if all_variables:
        cache_file.unlink(missing_ok=True)


@st.cache(suppress_st_warning=True)
def start_app() -> None:
    clear_cache()


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

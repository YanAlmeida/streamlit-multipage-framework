from collections import defaultdict
from typing import List, Any, Dict
from pathlib import Path

import streamlit as st

try:
    import joblib
    pickling = joblib
except ImportError:
    import pickle
    pickling = pickle


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
    pickling.dump(data, cache_file)


def load() -> Dict[str, Any]:
    if not cache_file.exists():
        return defaultdict(dict)

    return pickling.load(cache_file)

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

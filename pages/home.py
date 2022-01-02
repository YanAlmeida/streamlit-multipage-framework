from pathlib import Path

import streamlit as st


def startpage():
	st.markdown(Path("README.md").read_text())

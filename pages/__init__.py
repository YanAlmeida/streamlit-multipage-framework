from .home import startpage
from .save_variables import save_app
from .sum_variables import sum_variables
from .multiply_variables import multiply_variables

start_page = startpage

pages = {
    "App1": save_app,
    "App2": sum_variables,
    "App3": multiply_variables,
}

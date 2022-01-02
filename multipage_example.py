from multipage import MultiPage, start_app
from pages import pages, start_page

start_app()

app = MultiPage()
app.initial_page = start_page
app.start_button = "Let's go!"
app.navbar_name = "Navigation"
app.next_page_button = "Next Page"
app.previous_page_button = "Previous Page"

for app_name, app_function in pages.items():
    app.add_app(app_name, app_function)

app.run()

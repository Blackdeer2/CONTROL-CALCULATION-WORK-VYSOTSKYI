import flet as ft
from flet import Page, View, AppBar, ElevatedButton, Text, TextField
from UI import singup_page, log_in_page
from UI.user_page import user_page


def main_page(page: ft.Page):
    return ft.View(
        "/",
        [
            ft.AppBar(title=ft.Text("Main Page")),
            ft.Text("Welcome to the main page!"),
            ft.ElevatedButton(
                "Sign Up",
                on_click=lambda _: page.go("/sign_up")
            ),
            ft.ElevatedButton(
                "Log in",
                on_click=lambda _: page.go("/log_in")
            ),
        ],
    )

def main_UI(page: ft.Page, cursor):
    page.title = "Navigation Example"
    
    def route_change(e):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(main_page(page))
        
        elif page.route == "/sign_up":
            page.views.append(singup_page.sign_up(page, cursor))

        elif page.route == "/log_in":
            page.views.append(log_in_page.log_in(page, cursor))
        
        elif page.route.startswith("/user"):
            user_name = page.route.split("?name=")[-1]
            page.views.append(user_page(page, cursor, user_name))
        
        page.update()
    
    page.on_route_change = route_change

    page.go("/")



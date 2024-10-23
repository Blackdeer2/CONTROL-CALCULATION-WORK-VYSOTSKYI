import flet as ft
import hashlib
import BILL.functions as functions
import UI.close_banner_pop as close_banner_pop

def handle_login(page,cursor, user_name: str, password: str):
    if not user_name or not password:
        close_banner_pop.show_error_banner(page, "User name and password are required.")
        return
    result = functions.login(cursor,user_name, password)
    if result == user_name:
        return True
    
    if result is None:
        close_banner_pop.show_error_banner(page, "Invalid password. Please try again.")

    if result == "User does not exist.":
        close_banner_pop.show_error_banner(page, "User does not exist.")

def log_in(page: ft.Page, cursor):
    page.adaptive = True

    page.appbar = ft.AppBar(
        title=ft.Text("Log in"),
        bgcolor=ft.colors.with_opacity(0.04, ft.cupertino_colors.SYSTEM_BACKGROUND),
    )
    
    user_name_field = ft.TextField(keyboard_type=ft.KeyboardType.TEXT)
    password_field = ft.TextField(keyboard_type=ft.KeyboardType.TEXT, password=True)
    confirm_button = ft.FilledButton(content=ft.Text("Confirm"))
    back_button = ft.TextButton(content=ft.Text("Back"))

    def on_confirm_click(e):
        user_name = user_name_field.value
        password = password_field.value
        if handle_login(page, cursor, user_name, password):
            page.go(f"/user?name={user_name}")

    def on_signup_click(e):
        page.go("/")

    confirm_button.on_click = on_confirm_click
    back_button.on_click = on_signup_click

    return ft.View(
        "/sign_up",
        [
            ft.SafeArea(
                ft.Column(
                    [
                        ft.Text("User name:"),
                        user_name_field,
                        ft.Text("Password:"),
                        password_field,
                        confirm_button,
                        back_button
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
        ]
    )

def test(page: ft.Page):
    return ft.View(
        "/sign_up",
        [
            ft.AppBar(title=ft.Text("Log in Page")),
            ft.Text("This is the Sign Up page."),
            ft.ElevatedButton(
                "Back to Main Page",
                on_click=lambda _: page.go("/")
            ),
        ]
    )

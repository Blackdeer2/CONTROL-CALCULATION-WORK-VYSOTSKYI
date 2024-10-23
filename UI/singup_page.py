import flet as ft
import BILL.functions as functions
import UI.close_banner_pop as close_banner_pop

def handle_signup(page,cursor, user_name: str, password: str):
    if not user_name or not password:
        close_banner_pop.show_error_banner(page, "User name and password are required.")
        return
    result = functions.create_user(cursor, user_name, password)
    return result


def sign_up(page: ft.Page, cursor):
    user_name_field = ft.TextField(keyboard_type=ft.KeyboardType.TEXT)
    password_field = ft.TextField(keyboard_type=ft.KeyboardType.TEXT, password=True)
    confirm_button = ft.FilledButton(content=ft.Text("Confirm"))
    back_button = ft.TextButton(content=ft.Text("Back"))

    def on_back(e):
        page.go("/")

    def on_confirm_click(e):
        user_name = user_name_field.value
        password = password_field.value
        if handle_signup(page,cursor, user_name, password):
            page.go(f"/user?name={user_name}")

    confirm_button.on_click = on_confirm_click
    back_button.on_click = on_back
    
    return ft.View(
        "/sign_up",
        [
            ft.AppBar(
                title=ft.Text("Sign up"),
                bgcolor=ft.colors.with_opacity(0.04, ft.cupertino_colors.SYSTEM_BACKGROUND),
            ),
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
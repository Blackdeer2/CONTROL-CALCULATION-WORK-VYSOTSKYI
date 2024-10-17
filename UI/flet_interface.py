import flet as ft
import hashlib
import functions

# Example function for handling sign-up logic
def handle_signup(cursor, user_name: str, password: str):
    if not user_name or not password:
        print("User name and password are required.")
        return
    functions.create_user(cursor, user_name, password)

def singUp(page: ft.Page, cursor):
    page.adaptive = True

    page.appbar = ft.AppBar(
        title=ft.Text("Sign up"),
        bgcolor=ft.colors.with_opacity(0.04, ft.cupertino_colors.SYSTEM_BACKGROUND),
    )
    
    # Create text fields and button
    user_name_field = ft.TextField(keyboard_type=ft.KeyboardType.TEXT)
    password_field = ft.TextField(keyboard_type=ft.KeyboardType.TEXT, password=True)  # password=True hides the input
    confirm_button = ft.FilledButton(content=ft.Text("Confirm"))

    # Define what happens when the confirm button is clicked
    def on_confirm_click(e):
        user_name = user_name_field.value
        password = password_field.value
        handle_signup(cursor, user_name, password)

    # Assign the click event handler
    confirm_button.on_click = on_confirm_click

    # Add all components to the page
    page.add(
        ft.SafeArea(
            ft.Column(
                [
                    ft.Text("User name:"),
                    user_name_field,
                    ft.Text("Password:"),
                    password_field,
                    confirm_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
    )

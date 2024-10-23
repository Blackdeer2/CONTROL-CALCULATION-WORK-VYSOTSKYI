import flet as ft
import BILL.functions as functions
import UI.close_banner_pop as close_banner_pop

def check_password(page, cursor, user_name: str, new_password: str):
    if not new_password:
        close_banner_pop.show_error_banner(page, "Password are required.")
        return
    check_by_time =functions.can_change_password(cursor, user_name)
    if check_by_time == False:
        close_banner_pop.show_error_banner(page, "You can change your password only once a day.")
        return
    check_by_time = functions.is_password_expired(cursor, user_name)
    if check_by_time == True:
        close_banner_pop.show_error_banner(page, "Password has expired. Please change your password.")
        return
    result = functions.createNewPassword(cursor,user_name, new_password)
    if result == "New password must not match any of the previous passwords.":
        close_banner_pop.show_error_banner(page, result)
    if result == "Password is not secure.":
        close_banner_pop.show_error_banner(page, result)
    if result == "Password updated successfully.":
        close_banner_pop.show_success_banner(page, result)


def user_page(page: ft.Page, cursor, user_name: str):
    new_password_field = ft.TextField(keyboard_type=ft.KeyboardType.TEXT, password=True)
    сhange_button = ft.FilledButton(content=ft.Text("Change password"))

    def on_check_password(e):
        new_password = new_password_field.value
        check_password(page, cursor, user_name, new_password)

    сhange_button.on_click = on_check_password

    return ft.View(
        "/user",
        [
            ft.AppBar(title=ft.Text(f"Welcome, {user_name}!")),
            ft.Text(f"Hello, {user_name}! This is your personalized page."),
            new_password_field,
            сhange_button,
            ft.ElevatedButton(
                "Log out",
                on_click=lambda _: page.go("/")
            ),
        ]
    )

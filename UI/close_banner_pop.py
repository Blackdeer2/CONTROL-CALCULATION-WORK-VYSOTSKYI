import flet as ft

def show_error_banner(page: ft.Page, error_message: str):
    def close_banner(e):
        page.banner.open = False
        page.update()
        page.add(ft.Text("Action clicked: " + e.control.text))
    
    action_button_style = ft.ButtonStyle(color=ft.colors.BLUE)
    page.banner = ft.Banner(
        bgcolor=ft.colors.AMBER_100,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
        content=ft.Text(
            value=error_message,
            color=ft.colors.BLACK,
        ),
        actions=[
            ft.TextButton(text="Cancel", style=action_button_style, on_click=close_banner),
        ],
        open=True 
    )
    page.update()

def show_success_banner(page: ft.Page, success_message: str):
    def close_banner(e):
        page.banner.open = False
        page.update()
        page.add(ft.Text("Action clicked: " + e.control.text))
    
    action_button_style = ft.ButtonStyle(color=ft.colors.GREEN)
    page.banner = ft.Banner(
        bgcolor=ft.colors.LIGHT_GREEN_100,
        leading=ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE, color=ft.colors.GREEN, size=40),
        content=ft.Text(
            value=success_message,
            color=ft.colors.BLACK,
        ),
        actions=[
            ft.TextButton(text="Okay", style=action_button_style, on_click=close_banner),
        ],
        open=True
    )
    page.update()
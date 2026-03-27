import flet as ft

def main(page: ft.Page):
    # 1. Simulate a Mobile Screen Size
    page.window_width = 400
    page.window_height = 800
    page.title = "Guard App - Mobile View"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    
    # Center everything horizontally on the screen
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 2. Header
    header = ft.Text("Gate Scanner App", size=24, weight="bold", color=ft.Colors.BLUE_700)

    # 3. Driver Profile Card (Placeholder)
    # Notice how we removed 'name=' from ft.Icon to fix the error!
    photo_placeholder = ft.Container(
        width=150,
        height=150,
        bgcolor=ft.Colors.GREY_300,
        border_radius=75, # This makes the box a perfect circle
        content=ft.Icon(ft.Icons.PERSON, size=80, color=ft.Colors.GREY_500),
        alignment=ft.alignment.center
    )
    
    # Driver text info
    driver_info = ft.Column(
        controls=[
            ft.Text("Juan Dela Cruz", size=22, weight="bold"),
            ft.Text("Plate: ABC-1234", size=18, color=ft.Colors.GREY_700),
            ft.Text("Status: Waiting at Gate...", size=16, color=ft.Colors.ORANGE_500),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER # Centers the text
    )

    # 4. Action Buttons for the Guard
    inbound_btn = ft.ElevatedButton(
        text="Log Inbound Cargo", 
        icon=ft.Icons.LOGIN,
        bgcolor=ft.Colors.GREEN_600,
        color=ft.Colors.WHITE,
        width=300,
        height=50
    )
    
    outbound_btn = ft.ElevatedButton(
        text="Log Outbound Empty", 
        icon=ft.Icons.LOGOUT,
        bgcolor=ft.Colors.RED_600,
        color=ft.Colors.WHITE,
        width=300,
        height=50
    )

    # 5. Assemble the Vertical Mobile Layout
    mobile_layout = ft.Column(
        controls=[
            header,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT), # Invisible spacer
            photo_placeholder,
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT), 
            driver_info,
            ft.Divider(height=40, color=ft.Colors.TRANSPARENT), 
            inbound_btn,
            outbound_btn
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Add everything to the screen
    page.add(mobile_layout)

# Launch the app
ft.run(main)
import flet as ft

def main(page: ft.Page):
    # Setup the Page
    page.title = "Logistics & Driver RFID System - Admin Dashboard"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # 1. Header (Fixed: ft.Colors with a capital C)
    header = ft.Text("Warehouse Admin Dashboard", size=32, weight="bold", color=ft.Colors.BLUE_700)

    # 2. Table of Drivers
    drivers_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Driver Name")),
            ft.DataColumn(ft.Text("Plate Number")),
            ft.DataColumn(ft.Text("Status")),
        ],
        rows=[
            ft.DataRow(cells=[ft.DataCell(ft.Text("Juan Dela Cruz")), ft.DataCell(ft.Text("ABC-1234")), ft.DataCell(ft.Text("Inside"))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Maria Santos")), ft.DataCell(ft.Text("XYZ-9876")), ft.DataCell(ft.Text("Departed"))]),
        ]
    )

    # 3. Live Logs Box (Fixed: ft.Colors with a capital C)
    live_logs = ft.Container(
        content=ft.Text("Waiting for RFID taps...", color=ft.Colors.GREY_600),
        bgcolor=ft.Colors.GREY_200,
        padding=20,
        border_radius=10,
        height=200,
        width=300
    )

    # 4. Organize Layout (Side-by-Side)
    main_layout = ft.Row(
        controls=[
            # Left side: Drivers Table
            ft.Column([ft.Text("Registered Drivers", size=20, weight="bold"), drivers_table], expand=True),
            # Right side: Live Logs
            ft.Column([ft.Text("Live Logs", size=20, weight="bold"), live_logs])
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START
    )

    # Add everything to the screen
    page.add(header, ft.Divider(), main_layout)

# Run the app (Fixed: changed app() to run() to remove the warning)
ft.run(main)
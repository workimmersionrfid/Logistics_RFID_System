import flet as ft
import requests

# 🚨 PASTE YOUR REAL URL HERE! 🚨
FIREBASE_URL = "https://logistics-rfid-system-default-rtdb.asia-southeast1.firebasedatabase.app/"

def main(page: ft.Page):
    # --- RESPONSIVE PAGE SETTINGS ---
    page.title = "iAcademy Logistics Admin"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.padding = 20
    page.scroll = ft.ScrollMode.ADAPTIVE 

    # --- UI HEADER ---
    header_row = ft.Row(
        controls=[
            ft.Icon(ft.Icons.DASHBOARD_CUSTOMIZE, color=ft.Colors.CYAN_800, size=30),
            ft.Text("Live Logistics Monitor", size=26, weight="bold", color=ft.Colors.BLUE_900),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True 
    )

    # --- MOBILE RESPONSIVE CARD CONTAINER ---
    logs_container = ft.Column(spacing=15, scroll=ft.ScrollMode.ADAPTIVE)

    # --- CLOUD FETCHING LOGIC ---
    def fetch_logs(e=None):
        try:
            response = requests.get(FIREBASE_URL + "logs.json")
            data = response.json()

            logs_container.controls.clear() 

            if data:
                # Loop backwards to show newest first
                for log_id in reversed(list(data.keys())):
                    log = data[log_id]

                    status_text = log.get('delivery_status', 'N/A')
                    status_color = ft.Colors.GREEN_700 if "Successful" in status_text else ft.Colors.RED_700

                    # 1. Extract the GPS Coordinates
                    lat = log.get('latitude', 'N/A')
                    lon = log.get('longitude', 'N/A')

                    # 2. Create the Live Map Tracking Button (FIXED: removed 'text=')
                    track_btn = ft.ElevatedButton(
                        "Live Map Tracking", 
                        icon=ft.Icons.MAP,
                        bgcolor=ft.Colors.TEAL_600,
                        color=ft.Colors.WHITE,
                        url=f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                    )

                    # 3. Exception Handling: Disable the button if it's an old log without GPS data
                    if lat == "N/A" or lon == "N/A":
                        track_btn.disabled = True
                        track_btn.text = "No GPS Data Available"
                        track_btn.bgcolor = ft.Colors.BLUE_GREY_200
                        track_btn.url = None # Remove the link if there is no data

                    # --- BUILD THE CARD ---
                    log_card = ft.Card(
                        elevation=4,
                        content=ft.Container(
                            padding=20,
                            bgcolor=ft.Colors.WHITE, 
                            border_radius=10,
                            content=ft.Column([
                                ft.Text(f"⏱ {log.get('timestamp', 'N/A')}", weight="bold", color=ft.Colors.BLUE_900, size=16),
                                ft.Divider(height=1, color=ft.Colors.BLUE_GREY_100),
                                ft.Text(f"👤 Driver: {log.get('driver_name', 'N/A')} ({log.get('plate_number', 'N/A')})", size=14),
                                ft.Text(f"📋 Task: {log.get('task', 'N/A')} - {log.get('action', 'N/A')}", size=14),
                                ft.Text(f"📍 Location: {log.get('location', 'N/A')}", size=14),
                                ft.Text(f"🚚 Status: {status_text}", weight="bold", color=status_color, size=14),
                                ft.Text(f"🗺️ GPS: {lat}, {lon}", size=14, color=ft.Colors.BLUE_GREY_500),
                                ft.Divider(height=1, color=ft.Colors.BLUE_GREY_100),
                                ft.Text(f"📎 Proof: {log.get('document_attached', 'None')}", size=14, italic=True),
                                ft.Text(f"💬 Notes: {log.get('comments', 'None')}", size=14, italic=True),
                                ft.Divider(height=5, color=ft.Colors.TRANSPARENT), 
                                track_btn 
                            ])
                        )
                    )
                    logs_container.controls.append(log_card)
        except Exception as ex:
            print(f"Error fetching logs: {ex}")
        
        page.update()

    # FIXED: removed 'text='
    refresh_btn = ft.ElevatedButton(
        "Refresh Live Data", 
        icon=ft.Icons.REFRESH, 
        bgcolor=ft.Colors.AMBER_700, 
        color=ft.Colors.WHITE,
        height=50,
        on_click=fetch_logs
    )
    
    # --- ASSEMBLE THE SCREEN ---
    page.add(
        header_row, 
        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
        ft.Row([refresh_btn], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        logs_container
    )
    
    fetch_logs() 

ft.run(main)